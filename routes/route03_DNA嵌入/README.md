# 路线 3：DNA 序列嵌入提取（Route C / M1 特征）

## 功能
将 DNA 序列编码为向量（embedding），用于 gRNA 特征化 / 相似性检索。

- 模式1（首选）：DNABERT-2（HuggingFace）mean pooling 嵌入
- 模式2（降级）：k-mer(3) 直方图 + 随机投影（离线可用）

## 快速开始（Python 3.10）

```bash
# 交互式（stdin 逐行序列）
echo "ATGCAAGGCAAACTGCTGTAAGGTGGGGGA" | python routeC_embed.py

# 或使用包 API
python -c "from aicrispr.embeddings import embed; emb, mode = embed(['A'*30, 'C'*30]); print(mode, emb.shape)"
```

## 网络说明
- DNABERT-2 权重需 HuggingFace（zhihan1996/DNABERT-2-117M），网络受限时自动降级 k-mer
- 离线使用：设置 AICRISPR_DNABERT2=1 强制本地模式

## 依赖
numpy / torch / transformers（Python 3.10）

## 文献支撑
- DNABERT-2 (2024) ICLR
- DNA foundation benchmark (2025) Nat Commun
- 详见 docs/methods/RouteC_DNA预训练模型方法包.md
