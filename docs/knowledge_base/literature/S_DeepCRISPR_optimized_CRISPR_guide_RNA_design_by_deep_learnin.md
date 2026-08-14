# 文献卡：DeepCRISPR: optimized CRISPR guide RNA design by deep learning

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T1 gRNA效率 + T2 脱靶（on-target 与 off-target 统一框架） |
| 年份 | 2018 |
| 期刊 | Genome Biology |
| DOI | 10.1186/s13059-018-1459-4 |
| 项目映射 | M1（gRNA效率预测）、M2（脱靶评估） |

> 注：M1–M4/B1–B3/D 模块编号按项目背景（gRNA效率预测、脱靶评估、细胞工厂设计、LLM/Agent、基础支撑）推断映射。

## 1. 一句话核心
用"无监督预训练（DCDNN 去噪自编码器）→ CNN 混合网络微调"的深度框架，首次把 sgRNA 的 on-target 敲除效率预测与全基因组 off-target 图谱预测统一进一个模型，并用数据增强与 bootstrapping 平衡采样分别解决标注数据稀缺与 1:250 类别极不平衡问题，在 on-target 与 off-target 两项任务上全面超越当时的 SOTA 工具。

## 2. 方法要点（详细）
- **数据与编码**：
  - 无监督预训练数据：人类基因组全部 NGG PAM 的 20 bp sgRNA（编码区+非编码区），约 6.8 亿条，来自 ENCODE 13 种人类细胞系（HEK293、MCF-7、K562、HL60、NB4、BE2C、Caco-2、GM06990、Hela、HCT116、LNCap、HepG2、GM12878）；SPARK+GPU 大规模处理。
  - 编码方式："多通道图像"——核苷酸 4 通道（A/C/G/T）+ 每项表观特征 1 通道（CTCF ChIP-seq、H3K4me3 ChIP-seq、DNase-seq 染色质开放性、RRBS DNA 甲基化）＝8 通道区域表示。
  - on-target 标注数据：约 1.5 万条 sgRNA（hct116/hek293t/hela/hl60 四细胞系，1071 基因），敲除效率以 log fold change 定义；分类任务用 log2 fold change=1 阈值二值化；回归任务用协同过滤式矩阵归一化 ynorm = yij − (mrow+mcolumn+mall)/3 后再 rank 归一化，以整合多实验尺度。
  - 数据增强：在 5' 端前两个位置引入 2 个错配（已知不影响切割效率）并保持标签不变，把 1.5 万条种子扩充到约 20 万条非冗余 sgRNA。
  - off-target 数据：30 条 sgRNA（HEK293 系 18 条 + K562 12 条），bowtie2 全基因组检索得到约 16 万个"≤6 个错配"候选位点，其中真 off-target 约 700 个（正负比约 1:250；按错配数 1/2/3/4/5/6 分别为 4/31/121/236/174/75 个），来自 GUIDE-seq、Digenome-seq、BLESS、HTGTS、IDLV 五种检测平台。
- **模型架构**：DCDNN（deep convolutional denoising neural network）自编码器在大规模无标注 sgRNA 上做无监督表示学习 → 编码器作为预训练 parent network，与 CNN 拼接成混合网络并用标注数据微调（既学 CNN 权重也微调 parent 权重）。off-target 任务输入为"给定 sgRNA 编码 + 候选 off-target 位点编码"两部分，各过预训练编码器后 channel-wise 拼接再进 CNN（形成两个 baby network）。分类用 Softmax、回归用 Identity。
- **不平衡处理**：mini-batch 内对少数类（正样本）做 bootstrapping 采样至与多数类等量（1:1），稳定梯度更新。
- **评估**：分类（ROC-AUC、PR-AUC）与回归（Spearman、加权 Spearman，权重按 indel 频率排序）双 schema；设计了 8 个 on-target 测试场景（独立 20% 测试、预训练消融、增强消融、leave-one-cell-type-out、与重训 sgRNA Designer 的 apple-to-apple 对比、独立 HEL 数据集）和 3 个 off-target 场景（20% 独立测试、leave-sgRNA-group-out、30 折 leave-one-sgRNA-out）。
- **可解释性**：类特异性显著性图（对模型输出做梯度上升生成"合成 sgRNA"），配合 Fisher exact test 过滤统计不显著位点。

## 3. 关键结果与指标
- on-target 分类（四细胞系平均）：CNN 0.796 → 预训练 pt-CNN 0.836 → 预训练+增强 pt+aug 0.857（相对 sgRNA Designer 的 0.5 基线提升 113%/142%/157%）；leave-one-cell-type-out 平均 ROC-AUC 0.722（仍优于第二名 sgRNA Designer）；独立 HEL 细胞 425 条 sgRNA 回归测试中 Spearman 相关约为 sgRNA Designer 的近 2 倍，且超过专为该数据集设计的 CRISPRator。
- off-target 分类（20% 独立测试）：ROC-AUC 0.981、PR-AUC 0.497、Spearman 0.133、加权 Spearman 0.186，全面优于 CFD/MIT/CROP-IT/CCTop；leave-sgRNA-group-out：ROC-AUC 0.804、PR-AUC 0.303（CFD 仅 0.034）；30 折 leave-one-sgRNA-out：ROC-AUC 0.841、PR-AUC 0.421（CFD 0.333）——主要增益在降低假阳性。
- 自动特征发现结论：PAM NGG 变体位点偏好 C、回避 T；PAM 最近 4 个位置回避 T（多聚 U 降低 sgRNA 表达）；位置 18 偏好 C（切割位点）；偏好开放染色质（CTCF/DNase/H3K4me3）；回避 DNA 甲基化（RRBS）；off-target 显著性图分出三个核苷酸替换区——偏好区（位点 1–3）、未定区（4–15）、回避区（16–20），位点 16 的嘌呤-嘌呤错配（G→C、G→T）显著降低 off-target 活性。
- 定义 anti-OT 分数 S = ln(1+e^ΣP(OTi))/ln2（0,1]，用于全基因组综合脱靶评分，并用 Circos 图可视化脱靶谱。

## 4. 数据与代码可用性
- 平台 http://www.deepcrispr.net/；命令行代码 https://github.com/bm2-lab/DeepCRISPR；Zenodo: https://zenodo.org/record/1246320；Apache License 2.0；8 个附加文件（XLSX）含 on-target/off-target 数据、增强数据、特征显著性权重等。

## 5. 对我们项目的可借鉴点
1. **无监督预训练 + 微调范式**：用全基因组海量无标注 sgRNA 预训练可把标注稀疏任务提升 0.796→0.857——我们 E. coli 菌株改造中 sgRNA 实验标注极少，可先用 E. coli K-12/MG1655 基因组全 NGG 位点（约数十万条）做预训练再微调。
2. **数据增强策略**：PAM 远端（5' 端前 2 位）2 个错配不影响活性、标签不变——可直接用于扩充我们 E. coli gRNA 活性训练集（含文献已报道的 E. coli sgRNA 数据）。
3. **多通道"类图像"编码**：序列 one-hot + 表观特征各为独立通道；对大肠杆菌可把表观通道替换为 RNA-seq 表达水平、复制起点方向、GC 含量、操纵子位置等可获取特征。
4. **bootstrapping 1:1 平衡采样**：off-target 正负比 1:250 时在 mini-batch 内平衡正负样本，直接写入我们 M2 脱靶模块训练管线。
5. **显著性图自动化规则挖掘**：梯度上升显著性图输出"哪些位置/碱基偏好"的设计规则，可作为我们系统给用户的可解释设计建议（对接 LLM/报告模块）。
6. **anti-OT 综合评分 + Circos 可视化**：可作为我们 sgRNA 排序的子指标与全基因组脱靶展示组件。

## 6. 与我们方案的冲突/差异点
- DeepCRISPR 面向人源 SpCas9 NGG，且表观特征依赖人 ENCODE；大肠杆菌无染色质域/甲基化数据，需替换特征体系并重新预训练，不能直接迁移权重。
- 作者明确指出 off-target 任务分类模型优于回归模型（回归对数据量更敏感）——我们脱靶打分应以分类为主、回归为辅。
- 2018 年原型架构（CNN+自编码器）相对现代 DNA 语言模型有代差，适合做经典基线而非最终方案。

## 7. 行动项建议
- 将 DeepCRISPR 作为 M1/M2 经典基线复现（代码公开），在统一去泄漏协议下评估我们模型的相对提升。
- 采纳"无监督预训练+数据增强+bootstrapping"三件套到 E. coli sgRNA 效率/脱靶模型训练流程。
- 从其 GitHub/Zenodo 下载数据与显著性权重，登记进训练集清单，并在 README 数据来源章节引用。
