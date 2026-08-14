# 路线 2：CRISPR 脱靶预测（Route B / M2）

## 功能
给定 gRNA 与候选位点，预测脱靶风险（二分类）。

- 模型：双路架构 —— 序列 CNN（gRNA+候选 one-hot）+ 错配向量 MLP
- 特征：20 维错配指示 + (4,40) 拼接序列编码
- 支持：训练 / 推理 / 评估（AUROC/Accuracy）

## 快速开始（Python 3.10）

```bash
# 训练（CSV: grna,target,label）
python routeB_train.py --train pairs.csv --out out/

# 推理（CSV: grna,target）
python routeB_predict.py --predict pairs.csv --model out/model.pt
```

## 真实数据接入
- GUIDE-seq (Tsai 2015) / CIRCLE-seq (Kim 2017) 脱靶检测数据
- GEO GSE149363 等（需查证）

## 依赖
torch / numpy / scipy（Python 3.10）

## 文献支撑
- CRISPR-Net (2018) Bioinformatics
- DNABERT-Epi (2025) bioRxiv
- 详见 docs/methods/RouteB_脱靶预测方法包.md
