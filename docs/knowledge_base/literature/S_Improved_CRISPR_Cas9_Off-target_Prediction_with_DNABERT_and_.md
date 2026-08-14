# 文献卡：Improved CRISPR/Cas9 Off-target Prediction with DNABERT and Epigenetic Features

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T2 脱靶 |
| 年份 | 2025（bioRxiv 预印本，2025-04-22 发布，未经同行评审） |
| 期刊 | bioRxiv（预印本） |
| DOI | 10.1101/2025.04.16.649101 |
| 项目映射 | M2（脱靶评估） |

> 注：M1–M4/B1–B3/D 模块编号按项目背景（gRNA效率预测、脱靶评估、细胞工厂设计、LLM/Agent、基础支撑）推断映射。

## 1. 一句话核心
首次把预训练 DNA 语言模型 DNABERT（3-mer，MLM 预训练）引入 CRISPR/Cas9 脱靶预测：先做"错配位置预测"再微调"脱靶二分类"的两阶段微调，并叠加 H3K4me3/ATAC-seq/H3K27ac 表观特征形成 DNABERT-Epi；在 CHANGE-seq/GUIDE-seq 数据上与 5 个 SOTA 基线（GRU-Emb、CRISPR-BERT、CRISPR-HW、CRISPR-DIPOFF、CrisprBERT）对比，消融实验证明预训练与表观特征均显著有效，软投票集成模型全面最优。

## 2. 方法要点（详细）
- **数据**：CHANGE-seq（体外、110 条 sgRNA：202,040 活性 OTS / 4,734,238 非活性 OTS）；GUIDE-seq（细胞内、58 条 sgRNA：1,520 活性 / 2,118,820 非活性），均含 bulge 位点；正负比例约 1:23 与 1:1394（极端不平衡）；训练集负类随机降采样至 20%（固定随机种子、所有模型用同一份降采样数据），测试集保持原始分布。
- **三种实验场景**：S1 在 CHANGE-seq 上训练/测试；S2 在 GUIDE-seq 上训练/测试；S3 先在 CHANGE-seq 预训练再在 GUIDE-seq 微调并在其上测试（保证训练 sgRNA 与测试 sgRNA 无重叠防泄漏）。
- **交叉验证**：按 sgRNA 分组 10 折（Yaish et al. 方案），10 折×5 个随机种子重复，报告均值±标准差，Wilcoxon 符号秩检验显著性。
- **DNABERT 微调**：Hugging Face 3-mer DNABERT（12 层 Transformer、12 头注意力）；词表扩充加入 bulge 字符"-"的 3-mer token；输入格式 [CLS]+DNA 3-mer+[SEP]+sgRNA 3-mer+[SEP]；阶段一：错配位置预测任务（batch 8、lr 2e-5、5 epochs、随机 DNA-sgRNA 对）；阶段二：脱靶二分类（batch 256、lr 2e-5、5 epochs）；实现 transformers v4.48.3 + PyTorch v2.5.1。
- **DNABERT-Epi（筛选式多模态融合）**：先由微调后 DNABERT 打分，概率 ≥0.05 的样本进入表观融合模型；表观特征：以切割位点第一碱基为中心 ±500 bp（共 1000 bp）按 50 bp 分箱取均值→20 维+总体均值→21 维，H3K4me3/ATAC-seq/H3K27ac（GEO GSE149363）三特征拼接为 63 维；DNABERT 提取 CLS token、token 最大池化、token 均值池化三种 embedding，各自过 FNN(32)+ReLU+dropout(0.1)；表观特征同样过 FNN(32)；四路拼接成 128 维 → FNN(32)+ReLU+dropout → Softmax；训练 batch 256、lr 1e-4、5 epochs；推理：高概率样本取 DNABERT-Epi 与 DNABERT 输出平均，低概率样本直接用 DNABERT 输出。
- **基线**：GRU-Emb、CRISPR-BERT、CRISPR-HW、CRISPR-DIPOFF、CrisprBERT（按原论文在 PyTorch 2.5.1 重实现以保证同环境对比；epochs 10/30/30/50/10、batch 512/256/128/64/128、lr 5e-3/1e-4/3e-3/1e-4/2e-5；CrisprBERT 由 400 epochs 降至 10 防过拟合；CRISPR-DIPOFF/CrisprBERT 原不支持 bulge，已修改数据处理）；集成：软投票（概率平均）。
- **指标**：F1、MCC、ROC-AUC、PR-AUC（针对不平衡数据选型）。
- **可解释性**：可视化 12 层 Transformer 每层 12 头注意力均值，比较活性/非活性 OTS 的注意力差异。

## 3. 关键结果与指标
- S1（CHANGE-seq 内）：DNABERT ROC-AUC 0.9187 最高（p<0.01）；PR-AUC 上 CRISPR-BERT 与 CrisprBERT 最高；集成模型所有指标显著最优。
- S2（GUIDE-seq 内）：DNABERT-Epi 与 CRISPR-BERT 的 F1/MCC 最高（二者无显著差异）；DNABERT-Epi 的 PR-AUC 最高且显著优于 DNABERT；集成全面最优。
- S3（CHANGE-seq→GUIDE-seq 迁移）：DNABERT-Epi 的 F1/MCC 显著最高；CrisprBERT ROC-AUC 最高；PR-AUC 上 CrisprBERT 与 DNABERT-Epi 无显著差异；集成显著优于所有单模型。
- 预训练消融（S3）：预训练 DNABERT F1 0.4152±0.0928、MCC 0.4312±0.0766、ROC-AUC 0.9809±0.0118、PR-AUC 0.4554±0.0894；随机初始化模型全为 0.0000/0.0000/0.5182±0.0768/0.0076±0.0170（p≈3.8×10⁻¹⁰～8.9×10⁻¹⁶）——无预训练完全无法区分活性/非活性 OTS。
- 表观特征消融（S3）：含表观 vs 不含：F1 0.4302 vs 0.4257、MCC 0.4450 vs 0.4396、ROC-AUC 0.9809 vs 0.9809、PR-AUC 0.4612 vs 0.4579（全部 p<0.05，绝对幅度小但统计显著）。
- 注意力可视化：最后一层中活性 OTS 更关注序列后段（位置 10'–22'），非活性 OTS 更关注前段（1'–10'），与 Cas9 seed region 认识一致。
- 已知局限：5–6 个错配的高错配案例普遍被误分类为"非活性"，所有模型均受影响；表观特征带来的提升幅度有限，提示需补充 3D 结构、sgRNA 二级结构等信息。

## 4. 数据与代码可用性
- 代码（含 5 个基线重实现）：https://github.com/kimatakai/CRISPR_DNABERT；表观数据来源 GEO GSE149363；CHANGE-seq/GUIDE-seq 数据引用 Lazzarotto et al. 2020（Nat Biotechnol）与 Yaish et al. 2024（NAR）等原始文献（文中未提供直接下载链接）。

## 5. 对我们项目的可借鉴点
1. **DNA 语言模型预训练是数据稀缺场景的关键**：消融显示随机初始化完全失败（ROC-AUC 0.52），MLM 预训练几乎不可替代——我们可在 DNABERT 或自训 E. coli 基因组模型上微调脱靶任务，而不是从零训练深度模型。
2. **两阶段微调（错配位置预测→目标任务）**：先用中间任务给模型注入"错配位置"先验再学二分类，训练成本低、收敛好；可复用到我们 M2 脱靶与 M1 效率预测。
3. **筛选式多模态融合（DNABERT-Epi 架构）**：先序列模型筛出潜在正样本，再融合表观特征精排，避免全量高维特征拖慢训练；对大肠杆菌可用 RNA-seq 表达、复制起点、GC/操纵子位置等"原核表观"特征。
4. **负类降采样 20% + 固定种子**：1:1394 极端不平衡下保证每个 batch 有正样本且各模型可比——我们脱靶训练直接采用。
5. **按 sgRNA 分组 10 折 CV + 5 种子重复 + Wilcoxon 检验**：同 sgRNA 的位点必须同折防泄漏，多种子报告均值±标准差并做统计检验——作为我们 M2/B2 的标准评估协议。
6. **软投票集成**：即使移除性能最弱的 CRISPR-DIPOFF 也会掉点（S3 中 F1 0.4577 等指标下降），说明异质模型互补；我们可用"CNN+DNA语言模型+传统ML"三路集成提升鲁棒性。
7. **注意力可视化输出解释**：把"模型关注 seed 区"这类发现做成用户可读的解释（对接我们 LLM/报告模块）。

## 6. 与我们方案的冲突/差异点
- 本文为 2025 年 4 月 bioRxiv 预印本，未经同行评审，具体数值（尤其迁移场景）引用需谨慎并注明版本。
- 全部数据为人源体外/细胞内脱靶（CHANGE-seq/GUIDE-seq）；大肠杆菌基因组仅 ~4.6 Mb、无 GUIDE-seq 级数据，脱靶候选空间小得多，可考虑用体外 CIRCLE-seq/Digenome-seq 或 Cas-OFFinder 候选+实验验证构建 E. coli 专属数据。
- DNABERT 词表基于人基因组统计，迁移到 E. coli 需确认 3-mer 词表覆盖率并可能需增量预训练。
- 表观特征边际收益很小（PR-AUC +0.003），提示我们不应过度投资脱靶表观特征工程。

## 7. 行动项建议
- 将 CRISPR_DNABERT 代码（含 5 个基线重实现）纳入 M2 基线库，在 E. coli 脱靶数据上做迁移评估。
- 在训练管线中采用"预训练模型+两阶段微调+负类降采样+按 sgRNA 分组 CV"协议。
- 把"预训练必要性"与"集成收益"两条结论写入 README 模型选型依据章节。
