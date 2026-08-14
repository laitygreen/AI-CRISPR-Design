# 知识库 · 模块 01：gRNA 编辑效率预测（M1）

> 对应项目流程：候选 gRNA → M1 效率评分 → 排序 → 实验验证

## 1. 项目流程步骤
1. 数据集：整合 DeepCRISPR / CRISPRon / Doench 数据集 + 自产数据
2. 特征：序列 one-hot + 保守性 + 结构特征，或 DNA 预训练模型 embedding
3. 基线先行：CFD/MIT 规则评分 → XGBoost → CNN → 预训练底座微调
4. 评测：按基因划分留出集；Pearson r、AUROC、top-k 命中率
5. 输出：全基因组 gRNA 效率打分表

## 2. 文献支撑
| 文献 | 分级 | 支撑点 | PDF 已下载 |
|---|---|---|---|
| DeepCRISPR (2018) | S | 深度学习 gRNA 设计框架+数据集 | ✅ |
| CRISPRon/CRISPRoff (2021) | S | 数据整合+Transformer 效率预测 | ✅ |
| CRISPRscan (2015) | S | 序列特征-效率经验模型 | ⚠️ 需手动 |
| Doench 2016 (Azimuth) | S | 经典评分模型与数据集 | ⚠️ 需手动 |
| DNABERT-2 (2023) | S | DNA 预训练底座 | ⚠️ 需手动 |
| Nucleotide Transformer (2024) | S | 基因组预训练底座 | ⚠️ 需手动 |
| Cas13d DL prediction (2024) | S | 其他 Cas 系统的效率预测方法 | ⚠️ 需手动 |
| Transformer anti-noise (2023) | S | 抗噪 Transformer（数据噪声鲁棒） | ⚠️ 需手动 |
| Benchmarking DL CRISPR (2023) | A | 多模型公平对比基准 | ✅ |
| DL in CRISPR review (2023) | A | 方法全景综述 | ✅ |

## 3. 生信方法指导
- 数据格式：gRNA 20nt + PAM + 靶基因 + 效率标签（连续 0-1 或分档）
- 序列编码：one-hot(4×20)；DNABERT-2 k-mer tokenization（k=3/4/6 消融）
- 训练管线：PyTorch + HuggingFace transformers；LoRA 微调底座
- 数据划分：按基因分组（GroupKFold），防同源 gRNA 泄漏
- 特征组合：序列 + GC + 位置 + 保守性 + 表观（可选）

## 4. 大模型训练建议
- 底座选择：DNABERT-2（多物种，推荐）vs Nucleotide Transformer（500M 大）vs HyenaDNA（长上下文）
- 训练策略：冻结底座 + LoRA 微调分类/回归头；或全参微调（数据充足时）
- 损失：回归 MSE + 排序损失（listwise）组合
- 消融：报告 有/无 预训练底座、不同底座、不同特征组合的指标
- 评估重点：top-20 命中率（实验选 20 条验证）比全局 Pearson 更贴近实际使用

---

# 知识库 · 模块 02：脱靶风险评估（M2）

> 对应项目流程：候选 gRNA → M2 脱靶评分 → 特异性过滤 → 最终设计

## 1. 项目流程步骤
1. 数据：GUIDE-seq / CIRCLE-seq 实测脱靶 + 负样本（未脱靶位点）
2. 特征：错配数/位置、种子区错配、PAM 兼容性、位置加权
3. 模型：规则（CFD/MIT）→ 传统 ML → CNN/Transformer 分类
4. 评估：AUROC / AUPR / top-k 召回（漏检惩罚高）
5. 输出：每 gRNA 的脱靶位点清单与风险评分

## 2. 文献支撑
| 文献 | 分级 | 支撑点 | PDF 已下载 |
|---|---|---|---|
| GUIDE-seq (2015) | S | 脱靶检测金标准（数据采集方法） | ⚠️ 需手动 |
| CIRCLE-seq (2017) | S | 体外高敏脱靶检测 | ⚠️ 需手动 |
| Elevation (2018) | S | 脱靶预测模型（注意 DOI 需修正） | ⚠️ 需手动 |
| Improved off-target with DNABERT (2025) | S | DNABERT 特征+表观特征脱靶预测 | ✅ |
| Transformer anti-noise (2023) | S | 抗噪 Transformer 脱靶 | ⚠️ 需手动 |
| Data imbalance off-target (2020) | A | 脱靶数据不平衡处理 | ⚠️ 需手动 |
| DL CRISPR survey (2023) | A | 脱靶方法综述 | ✅ |

## 3. 生信方法指导
- 数据：每 gRNA 取全基因组候选位点（mm≤3），标记实测脱靶 Y/N
- 特征：错配位置向量（20 维）、PAM 类型、GC、种子区（8-12nt）加权
- 不平衡：脱靶为正样本极少 → SMOTE/加权损失/负样本抽样
- 比对：Bowtie2 或 BWA 生成候选位点；pysam 解析
- 评估：AUPR 优先（正样本稀少时 AUROC 会虚高）

## 4. 大模型训练建议
- 架构：CNN（序列）→ 全连接融合手工特征；或 Transformer 直接序列分类
- 预训练：DNABERT-2 embedding + 分类头（参考 Improved off-target with DNABERT）
- 多任务：效率+脱靶联合训练（共享底座，双头输出），可提升泛化
- 校准：温度缩放校准概率，输出校准后的风险阈值
- 业务指标：给定可接受脱靶率，最大化特异性（top-k 精确率）

