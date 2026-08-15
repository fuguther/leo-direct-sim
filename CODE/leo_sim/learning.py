"""Learning contracts for leo_sim (C1/C3/C4/C5/C6/C7) and canonical DDQN math.

Information boundary: every contract observes ONLY the current satellite's own
directly measured state plus its actually-arrived, non-expired local control
cache. C1 restricts the cache further to 1-hop origins; C3-C7 share exactly
the same information set (the vis_k cache) and differ only in
representation/aggregation and AoI handling.

Canonical Double-DQN target (dependency-independent, tested here):
    a* = argmax_a Q_online(s', a)   over legal (masked) actions only
    y  = r + gamma * (1 - done) * Q_target(s', a*)
Real TensorFlow training is gated: without a working TF runtime any learning
run fails closed (LearningUnavailable) — no mock stands in for migration.
"""
from __future__ import annotations

import importlib.util
import hashlib
import json
import math
import os
from collections import deque
from pathlib import Path

import numpy as np

try:
    import tensorflow as tf
except ImportError:  # pragma: no cover - exercised on TF-less hosts
    tf = None

CONTRACTS = ("C1", "C3", "C4", "C5", "C6", "C7", "GAT", "MPNN")

# per-origin feature block layout (all normalized):
#   [isl_queue_ratio, access_load_ratio, n_visible_cells_norm, aoi_norm]
ORIGIN_FEATURES = 4
# Destination-conditioning features appended to every contract's observation:
#   [dst_bearing_sin, dst_bearing_cos, dst_dist_norm]
# bearing is the azimuth of the destination in the local ENU tangent plane at
# the current satellite (N=0, E=90deg); distance is the great-circle distance
# from the satellite subpoint to the destination, normalized by 20000 km.
DEST_FEATURES = 3
_DEST_DIST_NORM_KM = 20000.0
_EARTH_R_KM = 6371.0
C3_DIM = 4 + ORIGIN_FEATURES            # own state + mean aggregate
C4_DIM = 4 + ORIGIN_FEATURES            # own + AoI-weighted aggregate
C5_DIM = 4 + ORIGIN_FEATURES + 1        # own + freshest entry + staleness flag
C6_MAX_HOPS = 4
C6_DIM = 4 + C6_MAX_HOPS * ORIGIN_FEATURES      # own + per-hop buckets
C7_MAX_ENTRIES = 5
C7_DIM = 4 + C7_MAX_ENTRIES * (ORIGIN_FEATURES + 1)  # own + AoI-ordered seq
C1_MAX_NEIGHBORS = 4
C1_DIM = 4 + C1_MAX_NEIGHBORS * ORIGIN_FEATURES

# Every contract appends the 3 destination-conditioning features.
CONTRACT_DIMS = {
    "C1": C1_DIM + DEST_FEATURES,
    "C3": C3_DIM + DEST_FEATURES,
    "C4": C4_DIM + DEST_FEATURES,
    "C5": C5_DIM + DEST_FEATURES,
    "C6": C6_DIM + DEST_FEATURES,
    "C7": C7_DIM + DEST_FEATURES,
}
ACTIONS = ("deliver", "N", "S", "E", "W")

# Graph-state contracts: real GAT / MPNN encoders consume a k-hop local
# subgraph, not a hand-rolled fixed aggregate.  These names are new: they do
# NOT reuse the V1 C4/C5 semantics (V2's C4/C5 are cache-aggregation rules).
GRAPH_MAX_NODES = 32
GRAPH_NODE_FEAT_DIM = 15
GRAPH_DIRS = ("N", "S", "E", "W")
GRAPH_CONTRACTS = ("GAT", "MPNN")


def graph_state_dim(max_nodes: int = GRAPH_MAX_NODES,
                    node_feat_dim: int = GRAPH_NODE_FEAT_DIM) -> int:
    """Flat width of a graph contract observation."""
    return (max_nodes * node_feat_dim
            + max_nodes * max_nodes
            + len(GRAPH_DIRS) * max_nodes
            + 4 + DEST_FEATURES)  # own-state tail + destination features


GRAPH_CONTRACT_DIMS = {c: graph_state_dim() for c in GRAPH_CONTRACTS}
CONTRACT_DIMS = dict(CONTRACT_DIMS)
CONTRACT_DIMS.update(GRAPH_CONTRACT_DIMS)


class LearningUnavailable(RuntimeError):
    """Learning execution requested without a real TensorFlow runtime."""


def require_tensorflow():
    """Fail closed unless a genuinely importable TensorFlow exists."""
    if tf is None:
        raise LearningUnavailable(
            "TensorFlow is not available in this environment; learning runs "
            "fail closed. Remaining gate: VM/TensorFlow verification.")
    return tf


class V2GraphEncoder(tf.keras.layers.Layer if tf is not None else object):
    """V2 GAT/MPNN graph encoder (module-level, serializable).

    Consumes the flattened observation built by ``build_graph_observation``:
      node features  [MAX_N, 15]
      adjacency      [MAX_N, MAX_N]   (adj[dst, src] = 1 for a real ISL edge)
      readout masks  [4, MAX_N]       (N/S/E/W first-hop grouping)
      own-state tail [4]
    Runs either GAT (multi-head attention) or MPNN (mean message passing)
    layers, then returns four directional readout embeddings concatenated
    with the own-state tail for a shared dense Q head.

    NOTE: this class references ``tf`` at import time, so this module may only
    be imported after ``require_tensorflow()`` succeeded.  ``TensorflowDDQN``
    calls ``require_tensorflow`` in ``__init__`` before the first use of the
    graph encoder, and fail-closed tests never import tf on TF-less hosts.
    """

    def __init__(self, enc_mode, n_nodes, f_dim, h_dim, layers, heads,
                 **kwargs):
        super().__init__(**kwargs)
        if enc_mode not in ("gat", "mpnn"):
            raise ValueError(
                f"graph encoder mode must be gat/mpnn, got {enc_mode!r}")
        if enc_mode == "gat" and int(h_dim) % int(heads) != 0:
            raise ValueError("GAT hidden_dim must be divisible by num_heads")
        self.enc_mode = enc_mode
        self.n_nodes = int(n_nodes)
        self.f_dim = int(f_dim)
        self.h_dim = int(h_dim)
        self.layers = int(layers)
        self.heads = int(heads)
        self.node_in = tf.keras.layers.Dense(
            self.h_dim, activation="relu", name="node_in")
        self.dir_default = self.add_weight(
            name="dir_default", shape=(4, self.h_dim),
            initializer="zeros", trainable=True)

    def get_config(self):
        cfg = super().get_config()
        cfg.update({
            "enc_mode": self.enc_mode,
            "n_nodes": self.n_nodes,
            "f_dim": self.f_dim,
            "h_dim": self.h_dim,
            "layers": self.layers,
            "heads": self.heads,
        })
        return cfg

    @classmethod
    def from_config(cls, config):
        return cls(
            enc_mode=config["enc_mode"], n_nodes=config["n_nodes"],
            f_dim=config["f_dim"], h_dim=config["h_dim"],
            layers=config["layers"], heads=config["heads"],
        )

    def build(self, input_shape):
        if self.enc_mode == "gat":
            hd = self.h_dim // self.heads
            self.gat_W = [
                self.add_weight(name=f"gat_{l}_W",
                                shape=(self.heads, self.h_dim, hd),
                                initializer="glorot_uniform",
                                trainable=True)
                for l in range(self.layers)]
            self.gat_a_src = [
                self.add_weight(name=f"gat_{l}_a_src",
                                shape=(self.heads, hd),
                                initializer="glorot_uniform",
                                trainable=True)
                for l in range(self.layers)]
            self.gat_a_dst = [
                self.add_weight(name=f"gat_{l}_a_dst",
                                shape=(self.heads, hd),
                                initializer="glorot_uniform",
                                trainable=True)
                for l in range(self.layers)]
            self.gat_self_W = [
                self.add_weight(name=f"gat_{l}_self_W",
                                shape=(self.h_dim, self.h_dim),
                                initializer="glorot_uniform",
                                trainable=True)
                for l in range(self.layers)]
            self.gat_bias = [
                self.add_weight(name=f"gat_{l}_bias",
                                shape=(self.h_dim,),
                                initializer="zeros", trainable=True)
                for l in range(self.layers)]
        else:
            self.msg_W = [
                self.add_weight(name=f"mpnn_{l}_msg_W",
                                shape=(self.h_dim, self.h_dim),
                                initializer="glorot_uniform",
                                trainable=True)
                for l in range(self.layers)]
            self.self_W = [
                self.add_weight(name=f"mpnn_{l}_self_W",
                                shape=(self.h_dim, self.h_dim),
                                initializer="glorot_uniform",
                                trainable=True)
                for l in range(self.layers)]
            self.mpnn_bias = [
                self.add_weight(name=f"mpnn_{l}_bias",
                                shape=(self.h_dim,),
                                initializer="zeros", trainable=True)
                for l in range(self.layers)]
        super().build(input_shape)

    def _parse(self, flat):
        n, f = self.n_nodes, self.f_dim
        node = tf.reshape(flat[:, :n * f], (-1, n, f))
        adj = tf.reshape(flat[:, n * f:n * f + n * n], (-1, n, n))
        readout = tf.reshape(
            flat[:, n * f + n * n:n * f + n * n + 4 * n],
            (-1, 4, n))
        tail = flat[:, n * f + n * n + 4 * n:]
        node_mask = node[:, :, 7:8]
        adj = adj * node_mask * tf.transpose(node_mask, [0, 2, 1])
        readout = readout * tf.transpose(node_mask, [0, 2, 1])
        return node, adj, readout, tail, node_mask

    def _gat_layer(self, h, adj, node_mask, l):
        heads, hd = self.heads, self.h_dim // self.heads
        Wh = tf.einsum("bnd,hdf->bhnf", h, self.gat_W[l])
        e_src = tf.reduce_sum(
            Wh * self.gat_a_src[l][None, :, None, :], axis=-1)
        e_dst = tf.reduce_sum(
            Wh * self.gat_a_dst[l][None, :, None, :], axis=-1)
        logits = tf.nn.leaky_relu(
            e_dst[:, :, :, None] + e_src[:, :, None, :], alpha=0.2)
        edge_mask = tf.cast(adj[:, None, :, :] > 0.0, tf.float32)
        logits = logits + (1.0 - edge_mask) * -1e9
        alpha = tf.nn.softmax(logits, axis=-1) * edge_mask
        denom = tf.reduce_sum(alpha, axis=-1, keepdims=True)
        alpha = alpha / tf.maximum(denom, 1e-9)
        msg = tf.matmul(alpha, Wh)
        msg = tf.transpose(msg, [0, 2, 1, 3])
        msg = tf.reshape(msg, (-1, self.n_nodes, heads * hd))
        out = tf.nn.relu(tf.matmul(h, self.gat_self_W[l]) + msg
                         + self.gat_bias[l])
        return out * node_mask

    def _mpnn_layer(self, h, adj, node_mask, l):
        src_msg = tf.matmul(h, self.msg_W[l])
        deg = tf.reduce_sum(adj, axis=-1, keepdims=True)
        msg = tf.matmul(adj, src_msg) / tf.maximum(deg, 1.0)
        out = tf.nn.relu(tf.matmul(h, self.self_W[l]) + msg
                         + self.mpnn_bias[l])
        return out * node_mask

    def call(self, flat, training=False):
        node, adj, readout, tail, node_mask = self._parse(flat)
        h = self.node_in(node) * node_mask
        for l in range(self.layers):
            if self.enc_mode == "gat":
                h = self._gat_layer(h, adj, node_mask, l)
            else:
                h = self._mpnn_layer(h, adj, node_mask, l)
        counts = tf.reduce_sum(readout, axis=-1, keepdims=True)
        dir_sum = tf.matmul(readout, h)
        dir_mean = dir_sum / tf.maximum(counts, 1.0)
        has_dir = tf.cast(counts > 0.0, tf.float32)
        dir_emb = has_dir * dir_mean \
            + (1.0 - has_dir) * self.dir_default[None, :, :]
        return tf.concat(
            [tf.reshape(dir_emb, (-1, 4 * self.h_dim)), tail], axis=1)


def _graph_custom_objects():
    return {"V2GraphEncoder": V2GraphEncoder}


class TensorflowDDQN:
    """Small shared-policy Double-DQN used by the V2 hop-by-hop runtime.

    The kernel, not the network, constructs the destination-aware legal mask
    from arrived local control state.  Consequently exploration cannot choose
    a hidden-global, looping, full-queue or geometrically unavailable action.
    One model is shared by all satellites, while every decision consumes only
    that satellite's local observation and legal mask.
    """

    def __init__(self, contract: str, cfg: dict, seed: int):
        if contract not in CONTRACT_DIMS:
            raise ValueError(f"unknown learning contract {contract!r}")
        self.tf = require_tensorflow()
        try:
            self.tf.config.experimental.enable_op_determinism()
        except Exception:
            pass
        self.tf.keras.utils.set_random_seed(int(seed))
        self.contract = contract
        self.input_dim = CONTRACT_DIMS[contract]
        self.cfg = dict(cfg)
        self.seed = int(seed)
        self.rng = np.random.default_rng(self.seed)
        self.replay = deque(maxlen=int(cfg["replay_size"]))
        self.mode = cfg["mode"]
        checkpoint = cfg.get("checkpoint_path")
        if checkpoint:
            path = Path(checkpoint)
            if not path.is_file():
                raise LearningUnavailable(f"DDQN checkpoint not found: {path}")
            actual_sha = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_sha != cfg.get("checkpoint_sha256"):
                raise LearningUnavailable(
                    "DDQN checkpoint SHA-256 differs from resolved config")
            self.online = self.tf.keras.models.load_model(
                path, compile=False, custom_objects=_graph_custom_objects())
            if tuple(self.online.input_shape) != (None, self.input_dim) \
                    or tuple(self.online.output_shape) != (None, len(ACTIONS)):
                raise LearningUnavailable(
                    "DDQN checkpoint shape does not match contract/actions")
            self.loaded_checkpoint = str(path.resolve())
            self.loaded_checkpoint_sha256 = actual_sha
        else:
            self.online = self._network()
            self.loaded_checkpoint = None
            self.loaded_checkpoint_sha256 = None
        self.target = self._network()
        self.target.set_weights(self.online.get_weights())
        self.optimizer = self.tf.keras.optimizers.Adam(
            learning_rate=float(cfg["lr"]))
        self.decisions = 0
        self.transitions = 0
        self.train_steps = 0
        self.last_loss = None
        # tf.function-compiled DDQN train step (bit-equivalent to the eager
        # path; ~5-6x faster). LEO_FAST_TRAIN=0 falls back to eager for
        # equivalence checks without changing the math.
        self._fast_enabled = os.environ.get("LEO_FAST_TRAIN", "1").strip() not in ("0", "false", "no")
        self._fast_train_fn = None
        self._fast_train_net_id = None
        self._fast_train_tgt_id = None

    def _network(self):
        tf = self.tf
        if self.contract in GRAPH_CONTRACTS:
            inp = tf.keras.layers.Input(shape=(self.input_dim,))
            x = V2GraphEncoder(
                enc_mode="gat" if self.contract == "GAT" else "mpnn",
                n_nodes=GRAPH_MAX_NODES, f_dim=GRAPH_NODE_FEAT_DIM,
                h_dim=64, layers=1, heads=2,
            )(inp)
            x = tf.keras.layers.Dense(64, activation="relu")(x)
            out = tf.keras.layers.Dense(len(ACTIONS), activation="linear")(x)
            return tf.keras.Model(inputs=inp, outputs=out)
        return tf.keras.Sequential([
            tf.keras.layers.Input(shape=(self.input_dim,)),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(len(ACTIONS), activation="linear"),
        ])

    def epsilon(self, now: float) -> float:
        if self.mode == "eval":
            return 0.0
        start = float(self.cfg["epsilon_start"])
        end = float(self.cfg["epsilon_end"])
        decay = float(self.cfg["epsilon_decay_s"])
        return end + (start - end) * math.exp(-max(0.0, float(now)) / decay)

    @staticmethod
    def _mask_array(mask: dict) -> np.ndarray:
        return np.asarray([bool(mask.get(a, False)) for a in ACTIONS], dtype=bool)

    def choose(self, observation: np.ndarray, mask: dict, now: float) -> str:
        legal = self._mask_array(mask)
        indices = np.flatnonzero(legal)
        if not len(indices):
            raise ValueError("DDQN decision requires at least one legal action")
        obs = np.asarray(observation, dtype=np.float32).reshape(1, self.input_dim)
        if self.rng.random() < self.epsilon(now):
            chosen = int(self.rng.choice(indices))
        else:
            q = self.online(obs, training=False).numpy()[0]
            chosen = int(indices[np.argmax(q[indices])])
        self.decisions += 1
        return ACTIONS[chosen]

    def remember(self, state, action: str, reward: float, next_state,
                 next_mask: dict, done: bool) -> None:
        if action not in ACTIONS:
            raise ValueError(f"unknown DDQN action {action!r}")
        transition = (
            np.asarray(state, dtype=np.float32), ACTIONS.index(action),
            float(reward), np.asarray(next_state, dtype=np.float32),
            self._mask_array(next_mask), bool(done),
        )
        self.replay.append(transition)
        self.transitions += 1
        if self.mode == "train" and len(self.replay) >= int(self.cfg["batch_size"]):
            self._train_once()

    def _train_once(self) -> None:
        batch_size = int(self.cfg["batch_size"])
        indices = self.rng.choice(len(self.replay), size=batch_size, replace=False)
        batch = [self.replay[int(i)] for i in indices]
        states = np.stack([x[0] for x in batch])
        actions = np.asarray([x[1] for x in batch], dtype=np.int64)
        rewards = np.asarray([x[2] for x in batch], dtype=np.float32)
        next_states = np.stack([x[3] for x in batch])
        masks = np.stack([x[4] for x in batch])
        dones = np.asarray([x[5] for x in batch], dtype=bool)
        if self._fast_enabled:
            fn = self._fast_train_fn
            if (fn is None or self._fast_train_net_id != id(self.online)
                    or self._fast_train_tgt_id != id(self.target)):
                fn = self._build_fast_train_fn()
                self._fast_train_fn = fn
                self._fast_train_net_id = id(self.online)
                self._fast_train_tgt_id = id(self.target)
            loss = fn(
                self.tf.convert_to_tensor(states, dtype=self.tf.float32),
                self.tf.convert_to_tensor(actions, dtype=self.tf.int64),
                self.tf.convert_to_tensor(rewards, dtype=self.tf.float32),
                self.tf.convert_to_tensor(next_states, dtype=self.tf.float32),
                self.tf.convert_to_tensor(~dones, dtype=self.tf.bool),
                self.tf.convert_to_tensor(masks, dtype=self.tf.bool),
            )
            self.last_loss = float(loss.numpy())
            self.train_steps += 1
            if self.train_steps % int(self.cfg["target_update_interval"]) == 0:
                self.target.set_weights(self.online.get_weights())
            return
        online_next = self.online(next_states, training=False).numpy()
        target_next = self.target(next_states, training=False).numpy()
        targets = ddqn_targets(
            online_next, target_next, masks, rewards, dones,
            float(self.cfg["gamma"]),
        ).astype(np.float32)
        with self.tf.GradientTape() as tape:
            q = self.online(states, training=True)
            chosen_q = self.tf.gather(q, actions, batch_dims=1)
            loss = self.tf.reduce_mean(self.tf.square(targets - chosen_q))
        grads = tape.gradient(loss, self.online.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.online.trainable_variables))
        self.train_steps += 1
        self.last_loss = float(loss.numpy())
        if self.train_steps % int(self.cfg["target_update_interval"]) == 0:
            self.target.set_weights(self.online.get_weights())

    def _build_fast_train_fn(self):
        tf = self.tf
        net, tgt, opt = self.online, self.target, self.optimizer
        B = int(self.cfg["batch_size"])
        S = self.input_dim
        A = len(ACTIONS)
        gamma = float(self.cfg["gamma"])
        spec = [
            tf.TensorSpec([B, S], tf.float32),      # states
            tf.TensorSpec([B], tf.int64),           # actions
            tf.TensorSpec([B], tf.float32),         # rewards
            tf.TensorSpec([B, S], tf.float32),      # next states
            tf.TensorSpec([B], tf.bool),            # not_done
            tf.TensorSpec([B, A], tf.bool),         # next action mask
        ]

        @tf.function(input_signature=spec, reduce_retracing=True)
        def _step(states, actions, rewards, next_states, not_done, next_mask):
            online_next = net(next_states, training=False)
            target_next = tgt(next_states, training=False)
            safe_mask = tf.where(
                tf.reduce_any(next_mask, axis=1, keepdims=True),
                next_mask,
                tf.ones_like(next_mask),
            )
            masked_online = tf.where(
                safe_mask, online_next, tf.cast(-1e9, online_next.dtype))
            a_star = tf.argmax(masked_online, axis=1)
            bootstrap = tf.gather(target_next, a_star, batch_dims=1)
            bootstrap = tf.where(not_done, bootstrap, tf.zeros_like(bootstrap))
            expected = tf.stop_gradient(rewards + gamma * bootstrap)
            with tf.GradientTape() as tape:
                q = net(states, training=True)
                q_a = tf.gather(q, actions, batch_dims=1)
                loss = tf.reduce_mean(tf.square(q_a - expected))
            grads = tape.gradient(loss, net.trainable_variables)
            opt.apply_gradients(zip(grads, net.trainable_variables))
            return loss

        return _step

    def save_and_verify(self, directory: str | Path) -> dict:
        out = Path(directory)
        out.mkdir(parents=True, exist_ok=True)
        model_path = out / "online.keras"
        self.online.save(model_path)
        checkpoint_sha = hashlib.sha256(model_path.read_bytes()).hexdigest()
        loaded = self.tf.keras.models.load_model(
            model_path, compile=False, custom_objects=_graph_custom_objects())
        probe = np.linspace(-0.5, 0.5, self.input_dim, dtype=np.float32)[None, :]
        before = self.online(probe, training=False).numpy()
        after = loaded(probe, training=False).numpy()
        verified = bool(np.allclose(before, after, rtol=0.0, atol=1e-7))
        metadata = self.diagnostics()
        metadata.update({
            "schema": "leo-sim-ddqn/v1",
            "checkpoint": model_path.name,
            "checkpoint_sha256": checkpoint_sha,
            "checkpoint_verified": verified,
            "probe_max_abs_error": float(np.max(np.abs(before - after))),
        })
        (out / "metadata.json").write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if not verified:
            raise LearningUnavailable("saved DDQN checkpoint failed load/prediction verification")
        return metadata

    def diagnostics(self) -> dict:
        return {
            "algorithm": "ddqn",
            "contract": self.contract,
            "mode": self.mode,
            "loaded_checkpoint": self.loaded_checkpoint,
            "loaded_checkpoint_sha256": self.loaded_checkpoint_sha256,
            "actions": list(ACTIONS),
            "decisions": self.decisions,
            "transitions": self.transitions,
            "train_steps": self.train_steps,
            "replay_size": len(self.replay),
            "last_loss": self.last_loss,
            "seed": self.seed,
        }


def own_state(slots_used: int, slots_cap: int, isl_queue_bits: dict,
              isl_queue_cap: int, n_visible: int, n_cells: int) -> np.ndarray:
    total_q = sum(isl_queue_bits.values())
    max_q = max(1, isl_queue_cap * max(1, len(isl_queue_bits)))
    return np.array([
        slots_used / max(1, slots_cap),
        total_q / max_q,
        n_visible / max(1, n_cells),
        1.0,  # bias/valid flag marking real own measurement
    ], dtype=np.float64)


def _origin_features(entry, now: float, isl_queue_cap: int) -> np.ndarray:
    p = entry.payload
    q = sum(p.get("isl_queue_bits", {}).values())
    used = p.get("access_slots_used", 0)
    cap = max(1, p.get("access_slots_cap", 1))
    nvis = len(p.get("visible_cells", ()))
    aoi = max(0.0, entry.aoi(now))
    return np.array([
        q / max(1, isl_queue_cap * 4),
        used / cap,
        min(1.0, nvis / 10.0),
        min(1.0, aoi / max(entry.ttl_s, 1e-9)),
    ], dtype=np.float64)


def destination_features(sat_lat_deg: float, sat_lon_deg: float,
                         dst_lat_deg: float, dst_lon_deg: float) -> np.ndarray:
    """3-dim destination features: ENU bearing (sin/cos) + great-circle dist."""
    sat_lat = math.radians(float(sat_lat_deg))
    sat_lon = math.radians(float(sat_lon_deg))
    dst_lat = math.radians(float(dst_lat_deg))
    dst_lon = math.radians(float(dst_lon_deg))

    # Destination vector in ENU at the satellite subpoint.
    dx = (_EARTH_R_KM * math.cos(dst_lat) * math.cos(dst_lon)
          - _EARTH_R_KM * math.cos(sat_lat) * math.cos(sat_lon))
    dy = (_EARTH_R_KM * math.cos(dst_lat) * math.sin(dst_lon)
          - _EARTH_R_KM * math.cos(sat_lat) * math.sin(sat_lon))
    dz = (_EARTH_R_KM * math.sin(dst_lat)
          - _EARTH_R_KM * math.sin(sat_lat))
    east = (-math.sin(sat_lon) * dx + math.cos(sat_lon) * dy)
    north = (-math.sin(sat_lat) * math.cos(sat_lon) * dx
             - math.sin(sat_lat) * math.sin(sat_lon) * dy
             + math.cos(sat_lat) * dz)
    bearing = math.atan2(east, north)

    # Great-circle distance (haversine).
    dlat = dst_lat - sat_lat
    dlon = dst_lon - sat_lon
    a = (math.sin(dlat / 2.0) ** 2
         + math.cos(sat_lat) * math.cos(dst_lat) * math.sin(dlon / 2.0) ** 2)
    dist_km = 2.0 * _EARTH_R_KM * math.asin(math.sqrt(min(1.0, a)))
    return np.array([
        math.sin(bearing),
        math.cos(bearing),
        min(1.0, dist_km / _DEST_DIST_NORM_KM),
    ], dtype=np.float64)


def information_set(contract: str, sat: int, cache, now: float,
                    topo, obs_hops: int | None = None) -> dict[int, object]:
    """The exact cache entries a contract may see.

    C1 always sees only 1-hop origins.  C3-C7 and the graph contracts see the
    same set: all valid arrived entries, optionally restricted to entries that
    travelled at most `obs_hops` hops (None = no hop restriction, i.e. the
    full vis_k cache).
    """
    entries = cache.valid_entries(now)
    if contract == "C1":
        allowed = {sat} | set(topo.get(sat, {}).values())
        return {o: e for o, e in entries.items() if o in allowed}
    if contract in ("C3", "C4", "C5", "C6", "C7", "GAT", "MPNN"):
        if obs_hops is None:
            return dict(entries)
        return {o: e for o, e in entries.items() if e.hops <= obs_hops}
    raise ValueError(f"unknown contract {contract!r}")


def _bfs_first_dirs(sat: int, topo: dict) -> dict[int, str]:
    """First-hop direction from `sat` to every reachable node in `topo`.

    BFS over the static ISL adjacency; the direction of the very first
    hop from the root labels each node (V1-style directional readout).
    Returns {node: first_dir}; the root itself is absent.
    """
    out: dict[int, str] = {}
    frontier = [(d, n) for d, n in sorted(topo.get(sat, {}).items())]
    for d, n in frontier:
        if n not in out and n != sat:
            out[n] = d
    next_frontier = [n for _d, n in frontier if n != sat]
    while next_frontier:
        further: list[int] = []
        for node in next_frontier:
            for d, n in sorted(topo.get(node, {}).items()):
                if n != sat and n not in out:
                    out[n] = out[node]
                    further.append(n)
        next_frontier = further
    return out


def _graph_node_features(origin: int, entry, root: int, first_dir: str,
                         topo: dict, isl_queue_cap: int,
                         root_pos: tuple = (0.0, 0.0, 0.0)) -> np.ndarray:
    """15-dim node feature for one subgraph node (V2 payload semantics)."""
    p = entry.payload if entry is not None else {}
    q = p.get("isl_queue_bits", {}) if entry is not None else {}
    used = p.get("access_slots_used", 0) if entry is not None else 0
    cap = max(1, p.get("access_slots_cap", 1)) if entry is not None else 1
    nvis = len(p.get("visible_cells", ())) if entry is not None else 0
    hop = entry.hops if entry is not None else 0
    pos = p.get("position", (0.0, 0.0, 0.0)) if entry is not None else (0.0, 0.0, 0.0)
    deg = sum(1 for _d, n in topo.get(origin, {}).items() if n is not None)
    feats = np.zeros(GRAPH_NODE_FEAT_DIM, dtype=np.float64)
    for i, d in enumerate(GRAPH_DIRS):
        feats[i] = min(1.0, q.get(d, 0) / max(1, isl_queue_cap))
    feats[4] = min(1.0, hop / max(1, 4))
    feats[5] = min(1.0, deg / max(1, len(GRAPH_DIRS)))
    feats[6] = 1.0 if origin == root else 0.0
    feats[7] = 1.0  # valid node flag (padding rows stay 0)
    if first_dir in GRAPH_DIRS:
        feats[8 + GRAPH_DIRS.index(first_dir)] = 1.0
    rel = np.asarray(pos, dtype=np.float64) - np.asarray(root_pos, dtype=np.float64)
    feats[12:15] = rel / 7000.0
    return feats


def build_graph_observation(contract: str, sat: int, cache, now: float,
                            topo: dict, own: np.ndarray,
                            isl_queue_cap: int = 256_000_000,
                            obs_hops: int | None = None,
                            dst_feats: np.ndarray | None = None) -> np.ndarray:
    """Fixed-width flattened k-hop subgraph for the GAT/MPNN contracts.

    Layout: node features [MAX_N, 15] + directed adjacency [MAX_N, MAX_N]
    + directional readout masks [4, MAX_N] + own-state tail [4].
    Nodes are the actually-arrived valid cache origins plus the root; only
    payload fields carried by arrived ControlPackets enter node features
    (no future geometry, no hidden global queues).
    """
    entries = information_set(contract, sat, cache, now, topo,
                              obs_hops=obs_hops)
    first_dirs = _bfs_first_dirs(sat, topo)
    n = GRAPH_MAX_NODES
    origins = sorted(set(entries) - {sat})
    nodes = [sat] + origins[:n - 1]
    overflow = max(0, len(origins) - (n - 1))
    index = {node: i for i, node in enumerate(nodes)}
    root_entry = entries.get(sat)
    root_pos = (root_entry.payload.get("position", (0.0, 0.0, 0.0))
                if root_entry is not None else (0.0, 0.0, 0.0))

    feats = np.zeros((n, GRAPH_NODE_FEAT_DIM), dtype=np.float64)
    for i, node in enumerate(nodes):
        entry = entries.get(node) if node != sat else None
        feats[i] = _graph_node_features(
            node, entry, sat, first_dirs.get(node), topo, isl_queue_cap,
            root_pos=root_pos)

    adj = np.zeros((n, n), dtype=np.float64)
    for dst, node in enumerate(nodes):
        for _d, nb in topo.get(node, {}).items():
            src = index.get(nb)
            if src is not None and src != dst:
                adj[dst, src] = 1.0

    readout = np.zeros((len(GRAPH_DIRS), n), dtype=np.float64)
    for i, node in enumerate(nodes):
        fd = first_dirs.get(node)
        if fd in GRAPH_DIRS:
            readout[GRAPH_DIRS.index(fd), i] = 1.0

    tail = np.asarray(own, dtype=np.float64).reshape(-1)
    if tail.shape[0] != 4:
        raise ValueError(f"graph tail requires a 4-dim own state, got {tail.shape}")
    df = (np.asarray(dst_feats, dtype=np.float64).reshape(-1)
          if dst_feats is not None else np.zeros(DEST_FEATURES))
    if df.shape[0] != DEST_FEATURES:
        raise ValueError(f"dst_feats must have {DEST_FEATURES} dims, got {df.shape}")
    tail = np.concatenate([tail, df])
    state = np.concatenate([feats.reshape(-1), adj.reshape(-1),
                            readout.reshape(-1), tail])
    expected = graph_state_dim()
    if state.shape[0] != expected:
        raise AssertionError(f"graph state width {state.shape[0]} != {expected}")
    return state


def build_observation(contract: str, sat: int, cache, now: float, topo,
                      own: np.ndarray, isl_queue_cap: int = 256_000_000,
                      obs_hops: int | None = None,
                      dst_feats: np.ndarray | None = None) -> np.ndarray:
    if contract in GRAPH_CONTRACTS:
        return build_graph_observation(
            contract, sat, cache, now, topo, own, isl_queue_cap,
            obs_hops=obs_hops, dst_feats=dst_feats)
    entries = information_set(contract, sat, cache, now, topo,
                              obs_hops=obs_hops)
    feats = {o: _origin_features(e, now, isl_queue_cap) for o, e in entries.items()}
    own = np.asarray(own, dtype=np.float64)
    df = (np.asarray(dst_feats, dtype=np.float64).reshape(-1)
          if dst_feats is not None else np.zeros(DEST_FEATURES))
    if df.shape[0] != DEST_FEATURES:
        raise ValueError(f"dst_feats must have {DEST_FEATURES} dims, got {df.shape}")

    def _finish(base: np.ndarray) -> np.ndarray:
        return np.concatenate([base, df])

    if contract == "C1":
        neighbors = sorted(set(topo.get(sat, {}).values()))
        blocks = [feats.get(n, np.zeros(ORIGIN_FEATURES)) for n in neighbors]
        blocks += [np.zeros(ORIGIN_FEATURES)] * (C1_MAX_NEIGHBORS - len(blocks))
        return _finish(np.concatenate([own] + blocks[:C1_MAX_NEIGHBORS]))

    if contract == "C3":
        agg = (np.mean(list(feats.values()), axis=0) if feats
               else np.zeros(ORIGIN_FEATURES))
        return _finish(np.concatenate([own, agg]))

    if contract == "C4":
        if not entries:
            agg = np.zeros(ORIGIN_FEATURES)
        else:
            w = np.array([np.exp(-max(0.0, e.aoi(now)) / max(e.ttl_s, 1e-9))
                          for e in entries.values()])
            agg = np.average(list(feats.values()), axis=0, weights=w)
        return _finish(np.concatenate([own, agg]))

    if contract == "C5":
        if not entries:
            return _finish(np.concatenate(
                [own, np.zeros(ORIGIN_FEATURES), [0.0]]))
        freshest = min(entries.values(), key=lambda e: e.aoi(now))
        return _finish(np.concatenate(
            [own, _origin_features(freshest, now, isl_queue_cap), [1.0]]))

    if contract == "C6":
        buckets = [[] for _ in range(C6_MAX_HOPS)]
        for o, e in entries.items():
            h = min(max(1, e.hops), C6_MAX_HOPS)
            buckets[h - 1].append(feats[o])
        blocks = [np.mean(b, axis=0) if b else np.zeros(ORIGIN_FEATURES)
                  for b in buckets]
        return _finish(np.concatenate([own] + blocks))

    if contract == "C7":
        ordered = sorted(entries.values(), key=lambda e: e.aoi(now))
        blocks = []
        for e in ordered[:C7_MAX_ENTRIES]:
            blocks.append(np.concatenate(
                [_origin_features(e, now, isl_queue_cap), [1.0]]))
        while len(blocks) < C7_MAX_ENTRIES:
            blocks.append(np.zeros(ORIGIN_FEATURES + 1))
        return _finish(np.concatenate([own] + blocks))

    raise ValueError(f"unknown contract {contract!r}")


def build_action_mask(can_deliver: bool, isl_room: dict) -> dict:
    """Legal actions: deliver only when directly visible with downlink room;
    each ISL direction only with queue room. Computed by the kernel from
    current local state only."""
    mask = {"deliver": bool(can_deliver)}
    for d, room in sorted(isl_room.items()):
        mask[d] = bool(room)
    return mask


def ddqn_targets(q_online_next: np.ndarray, q_target_next: np.ndarray,
                 next_mask: np.ndarray, rewards: np.ndarray,
                 dones: np.ndarray, gamma: float) -> np.ndarray:
    """Canonical Double-DQN targets.

    q_online_next, q_target_next: (batch, n_actions)
    next_mask: (batch, n_actions) bool, True = legal action
    rewards, dones: (batch,)
    """
    q_online_next = np.asarray(q_online_next, dtype=np.float64)
    q_target_next = np.asarray(q_target_next, dtype=np.float64)
    dones = np.asarray(dones, dtype=bool)
    masked = np.where(next_mask, q_online_next, -np.inf)
    a_star = np.argmax(masked, axis=1)
    selected = masked[np.arange(len(a_star)), a_star]
    # Terminal transitions do not bootstrap, so they do not need a legal
    # action in the next state.  Non-terminal rows still fail closed.
    if not np.all(np.isfinite(selected[~dones])):
        raise ValueError("every non-terminal transition must have at least one legal action")
    bootstrap = q_target_next[np.arange(len(a_star)), a_star]
    bootstrap = np.where(dones, 0.0, bootstrap)
    return rewards + gamma * bootstrap
