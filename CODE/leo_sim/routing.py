"""Routing policies for leo_sim.

Information boundary (binding):
- The deliver action uses only the current satellite's own direct, current
  visibility of the destination endpoint.
- hop/delay/capacity discover "who can see the destination cell" ONLY from
  the satellite's own local control cache (actually arrived, non-expired
  advertisements).
- Static constellation topology is a-priori knowledge; it is DIRECTED.
  Reachability and next-hop costs are computed over true directed edges only
  (reverse adjacency from the targets), never over silently mirrored links.
  Physical bidirectionality is verified once at topology construction.
- capacity additionally uses advertised queue state from the cache; the first
  hop uses the satellite's own directly observed queues.
- delay/capacity use directly observed propagation for the first hop and only
  arrived, non-expired advertised propagation for remote edges.  They never
  query global current geometry for a remote link.
- oracle is explicitly labeled an ANALYSIS UPPER BOUND: it may use global
  current knowledge (and may decide to wait). It never feeds learning.

No policy reads future ephemeris or hidden global queues.
"""
from __future__ import annotations

import heapq
from collections import deque

ORACLE_LABEL = "analysis_upper_bound"


def control_broadcast_children(topo, origin: int, max_hops: int) -> dict[int, list[str]]:
    """Build one deterministic shortest-path broadcast tree.

    Every reached satellite has exactly one parent, so one snapshot creates at
    most one real control-packet transmission per reached satellite.  This
    retains hop-by-hop propagation delay, queueing, bandwidth consumption and
    loss/expiry while avoiding exponential duplicate flooding on constellations
    with rings and cross-plane links.
    """
    if origin not in topo:
        raise ValueError(f"control origin {origin} absent from topology")
    if isinstance(max_hops, bool) or not isinstance(max_hops, int) or max_hops < 0:
        raise ValueError("control max_hops must be a non-negative integer")
    children: dict[int, list[str]] = {s: [] for s in topo}
    depth = {origin: 0}
    queue = deque([origin])
    while queue:
        node = queue.popleft()
        if depth[node] >= max_hops:
            continue
        # Peer id is the stable tie-breaker; direction breaks malformed
        # parallel-edge ties deterministically without inventing an edge.
        edges = sorted(topo.get(node, {}).items(), key=lambda item: (item[1], item[0]))
        for direction, peer in edges:
            if peer in depth:
                continue
            depth[peer] = depth[node] + 1
            children[node].append(direction)
            queue.append(peer)
    return children


def build_topology(geometry, num_sats: int, dirs) -> dict[int, dict[str, int]]:
    """Static a-priori neighbor graph; self-links are excluded.

    Physical ISLs are bidirectional, and that contract is VERIFIED here (fail
    closed): if a geometry provider hands us a one-way edge we refuse to build
    the topology rather than letting routing silently fabricate the reverse
    edge."""
    topo: dict[int, dict[str, int]] = {}
    for s in range(num_sats):
        nb = geometry.neighbors(s, dirs)
        topo[s] = {d: n for d, n in nb.items() if n != s}
    for s, nb in topo.items():
        for d, n in nb.items():
            if s not in topo.get(n, {}).values():
                raise ValueError(
                    f"ISL topology not bidirectional: {s}-{d}->{n} has no "
                    "reverse edge; refusing to fabricate one in routing")
    return topo


def _reverse_adj(topo) -> dict[int, set[int]]:
    """node -> its in-neighbours under the TRUE directed edges (no fabricated
    reverse links): x in radj[y] iff topo[x] contains an edge to y."""
    radj: dict[int, set[int]] = {s: set() for s in topo}
    for s, nb in topo.items():
        for n in nb.values():
            radj.setdefault(n, set()).add(s)
    return radj


def _multi_source_dist(adj, sources, edge_cost) -> dict[int, float]:
    dist = {s: float("inf") for s in adj}
    pq = []
    for s in sources:
        if s in dist:
            dist[s] = 0.0
            heapq.heappush(pq, (0.0, s))
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v in sorted(adj.get(u, ())):
            w = edge_cost(u, v)
            if w == float("inf"):
                continue
            nd = d + w
            if nd < dist[v] - 1e-15:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def destinations_in_cache(cache, dst_cell: str, now: float) -> list[int]:
    """Origins whose valid, actually-arrived advertisement reports CURRENT
    service capability (serve_cells) for dst_cell — visibility alone does
    not make a satellite a legal egress."""
    out = []
    for origin, entry in cache.valid_entries(now).items():
        if dst_cell in entry.payload.get("serve_cells", ()):
            out.append(origin)
    return sorted(out)


def choose_next_hop(policy: str, sat: int, dst_cell: str, now: float,
                    geometry, topo, cache, own_queue_bits: dict,
                    isl_rate_bps: float, prop_delay,
                    oracle_targets: list[int] | None = None,
                    best_only: bool = False) -> tuple[list[str], str]:
    """Return (ordered candidate directions, status).

    status: "ok" (candidates non-empty), "no_info" (no destination
    advertisement available), "unreachable" (advertised but no path).
    Only satellites advertising CURRENT service capability for dst_cell
    (serve_cells) count as legal egress; mere visibility is not enough.
    """
    if policy not in ("hop", "delay", "capacity", "oracle"):
        raise ValueError(f"unknown routing policy {policy!r}")

    if policy == "oracle":
        # analysis upper bound: caller passes the true current serving sats.
        targets = list(oracle_targets or [])
    else:
        targets = destinations_in_cache(cache, dst_cell, now)
    targets = [t for t in targets if t != sat]
    if not targets:
        return [], "no_info"

    # reachability and path cost follow the TRUE directed edges only: the
    # multi-source search expands backward from the targets over the reverse
    # adjacency, so dist[x] is the cost of a real directed path x -> target.
    # edge_cost(u, v) below is evaluated with u = popped node, v = predecessor
    # being relaxed, i.e. the forward edge v -> u.
    adj = _reverse_adj(topo)

    def observed_propagation(a, b):
        """Propagation metric available at `sat` for forward edge a -> b."""
        if a == sat:
            # A satellite directly observes its own incident link now.
            return prop_delay(geometry.isl_range_km(a, b, now))
        entry = cache.entry(a)
        if entry is None or not entry.valid_at(now):
            return None
        direction = _dir_of(topo, a, b)
        if direction is None:
            return None
        value = entry.payload.get("isl_propagation_s", {}).get(direction)
        if not isinstance(value, (int, float)) or value < 0:
            return None
        return float(value)

    if policy == "hop":
        fwd_cost = lambda a, b: 1.0  # noqa: E731
    elif policy == "oracle":
        # The explicitly labeled oracle uses perfect global current knowledge.
        def fwd_cost(a, b):
            return prop_delay(geometry.isl_range_km(a, b, now))
    elif policy == "delay":
        def fwd_cost(a, b):
            value = observed_propagation(a, b)
            return float("inf") if value is None else value
    else:  # capacity
        def fwd_cost(a, b):
            c = observed_propagation(a, b)
            if c is None:
                return float("inf")
            if a == sat:
                q = own_queue_bits  # directly observed local queues
                dir_ab = _dir_of(topo, a, b)
                qb = q.get(dir_ab, 0) if dir_ab else None
            else:
                entry = cache.entry(a)
                if entry is None or not entry.valid_at(now):
                    qb = None
                else:
                    dir_ab = _dir_of(topo, a, b)
                    qb = entry.payload.get("isl_queue_bits", {}).get(dir_ab) if dir_ab else None
            if qb is None:
                return float("inf")  # unknown queue state is not assumed free
            return c + qb / isl_rate_bps

    # dist[x] = forward cost from x to the nearest target; the search expands
    # backward from targets, so the forward edge cost is evaluated reversed.
    dist = _multi_source_dist(adj, targets, lambda u, v: fwd_cost(v, u))
    if dist.get(sat, float("inf")) == float("inf"):
        return [], "unreachable"
    scored = []
    for d, n in sorted(topo.get(sat, {}).items()):
        w = fwd_cost(sat, n)
        total = w + dist.get(n, float("inf"))
        if total < float("inf"):
            scored.append((total, d))
    scored.sort(key=lambda x: (x[0], x[1]))
    if best_only and scored:
        best = scored[0][0]
        scored = [item for item in scored
                  if abs(item[0] - best) <= 1e-12 * max(1.0, abs(best))]
    return [d for _c, d in scored], "ok"


def _dir_of(topo, a, b):
    for d, n in topo.get(a, {}).items():
        if n == b:
            return d
    return None
