# Q0 tiny 当前信息 DP 原型（2026-08-19）

## 定位

`CODE/leo_sim/q0_tiny.py` 是 Q0-I 的正确性锚点，不是正式实验求解器，也不是
Q0-F 的 clairvoyant 上界。它只用于验证：有限状态上的 Bellman 递推可以找到
字典序物理目标的最优动作序列，并且结果可以转换为现有 `JointPlan` 合同。

## 当前模型边界

- 所有包在 `t=0` 已知；无未来到达、GE、随机故障、动态拓扑和控制广告。
- 拓扑固定、有限、无自环且双向；每个时隙最多服务一个包动作。
- forward 和 deliver 都消耗一个离散时隙；等待只作为 DP 的隐式动作。
- 目标为 `(按 deadline 交付数, -完成时间总和, -等待时隙数)` 的字典序最大化。
- `JointPlan` 导出保留动作顺序和时刻分组，但仍需 kernel 的实时版本/物理校验；
  原型不能绕过 `validate_joint_plan` 或 `apply_joint_plan`。

## 证据与限制

- 测试覆盖两跳路径、deadline 优先、多包调度、非法 horizon/邻接和计划导出。
- 当前平台测试：`pytest -q CODE/leo_sim/tests` = `415 passed`。
- 该原型没有证明真实 SimPy kernel 的最优性，也没有完成 planned-vs-executed
  逐事件回放；在 Q0 合同（未来几何/流量、deadline 边界、控制范围）冻结前，
  不得生成或引用论文正式结果。

## 下一步

1. 将 tiny 图动作映射到真实卫星方向和真实 packet 状态，做 planned-vs-executed 逐事件核对。
2. 在同一 tiny 场景接入 Q0-F 的固定未来时间线，并与当前信息 DP 交叉验证。
3. 合同冻结后再决定是否实现 CP-SAT/MILP；大规模仍只能使用明确标注的近似参照。
