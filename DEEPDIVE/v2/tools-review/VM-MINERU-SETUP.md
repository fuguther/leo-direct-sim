# VM 文献处理环境（2026-09-05）

## 部署位置（VM: 192.168.200.23, 用户 liguang13, aarch64/Ubuntu24.04/A100 40GB）
- 统一文献库: /data/论文/papers-lib/PAPER-LIBRARY/（418M, 165文件: PDF106/MD18/TXT41, Zotero副本已并入)
- MinerU venv: /data/论文/papers-lib/mineru-venv/（python3.12, torch 2.10.0+cu126 + torchvision 0.29.0+cu126）
- 模型缓存: /data/论文/papers-lib/hf-cache/
- 提取脚本: /data/论文/papers-lib/pdf2md.sh

## 踩坑记录（复现必读）
1. VM 无 pip/sudo → 用 uv 建 venv（~/.local/bin/uv）
2. MinerU 3.x 的 torch 在 [pipeline] extra，需显式装
3. 缺 libGL.so.1 → opencv-python 换 opencv-python-headless
4. torch 2.14.0+cu130 与 VM 驱动 570(CUDA12.8) 不匹配，A100 是 aarch64 → 官方无 cu128 aarch64 wheel
   → 最终方案: torch==2.10.0+cu126-cp312-aarch64 + torchvision cu126(aarch64)，与驱动兼容
5. torchvision 必须同 cu126 源重装，否则 torchvision::nms 不存在
6. 批量跑 3 篇打包会失败，单篇跑稳定；指令模板见 /data/论文/papers-lib/run-batch.sh

## 使用
ssh vm "cd /data/论文/papers-lib && ./mineru-venv/bin/mineru -p <pdf> -o <outdir> -b pipeline -l en"
(单篇约 40s-2min(A100 GPU) vs 本地 mac CPU 单篇 1-2min)
