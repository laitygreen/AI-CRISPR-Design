# 路线 1：gRNA 编辑效率预测（Route A / M1）

## 功能
给定 20nt spacer + PAM 上下文（30mer），预测 gRNA 编辑效率（回归）。

- 模型：CRISPRon 风格多尺度 CNN（kernel 3/5/7）+ one-hot 30mer 编码
- 支持：训练 / 推理 / 评估（Pearson/Spearman/MAE）

## 快速开始（Python 3.10）

```bash
# 训练（CSV: seq,efficiency）
python routeA_train.py --train data.csv --out out/

# 推理（FASTA 30mers）
python routeA_predict.py --predict 30mers.fa --model out/model.pt

# 或使用包 API
python -c "from aicrispr.grna_efficiency import train, predict"
```

## 真实数据接入
- rth.dk CRISPRon 23902 条 gRNA 效率数据（需申请）
- Azimuth V1/V2 数据（本地 repos/Azimuth-master/azimuth/data/）

## 依赖
torch / numpy（Python 3.10）

## 文献支撑
- DeepCRISPR (2018) Genome Biology
- CRISPRon (2021) Nature Communications
- 详见 docs/methods/RouteA_gRNA效率预测方法包.md
