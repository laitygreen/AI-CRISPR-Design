# 文献卡：Benchmarking DNA foundation models for genomic and genetic tasks

| 字段 | 内容 |
|---|---|
| 分级 | A |
| 主题 | T3 DNA底座 |
| 年份 | 2025 |
| 期刊 | Nature Communications（2025, 16:10780） |
| DOI | 10.1038/s41467-025-65823-8 |
| 项目映射 | M1（gRNA效率预测的嵌入特征/底座选型）、M2（脱靶效应向量评估方法）、B2（生信多组学/特征工程管线）、B3（模型选型基线） |

## 1. 一句话核心
对 5 个主流 DNA 基础模型（DNABERT-2、Nucleotide Transformer V2、HyenaDNA、Caduceus-Ph、GROVER）在 57 个数据集、4 大类基因组/遗传任务（序列分类、基因表达预测、变异效应量化、TAD 识别）上做零样本嵌入的系统无偏基准，发现"平均 token 嵌入（mean token pooling）"稳定优于 [CLS]/[SEP] 摘要 token 和最大池化，且不同架构/预训练数据的模型在任务上各有强弱——通用基础模型在致病突变识别上意外胜出，但在基因表达与 QTL 因果变异上不如专用模型。

## 2. 方法要点（详细）
- **被评模型**：
  - DNABERT-2：BERT 架构 + ALiBi 位置编码，BPE 分词（可变 token 数），MLM 预训练于 135 物种基因组，约 117M 参数，嵌入维度 768，无硬性长度上限（实际运行时随长度二次增长）。
  - NT-v2（Nucleotide Transformer V2）：BERT 架构 + rotary 嵌入 + Swish 激活（无 bias），6-mer 滑窗分词（长度约 L/6），MLM 预训练于 850 物种，最大 500M 参数、1024 维、输入上限 12,000 nt。
  - HyenaDNA：无 attention 的 decoder 架构，Hyena 算子（长卷积 + 隐式参数化 + 数据控制门控），逐核苷酸单 token，仅人类参考基因组上的 next-nucleotide 预训练，约 30M 参数、256 维、最长 1M nt；支持 in-context soft-prompting。
  - Caduceus-Ph：MambaDNA（选择性状态空间模型 SSM）+ BiMamba 双向建模 + 反向互补（RC）等变模块（后处理 conjoining 方式合并双链预测），约 35M 参数、256 维、最长 131K nt。
  - GROVER：BERT 式 12 层 transformer，BPE 词表经 600 轮迭代优化，masked token 预测预训练于人类基因组，约 117M 参数、768 维，输入 512 token（平均约 2048 bp）。
- **基准数据**：57 个分类数据集（52 二元 + 5 多类），序列 41 bp ~ 2000 bp，分 4 类：人类基因组区分类（启动子/增强子/剪接位点/TFBS/开放染色质）、多物种基因组区分类（拟南芥、枯草芽孢杆菌、荚膜红细菌启动子等）、人类表观遗传修饰（5mC、6mA，41 bp 中心化序列）、多物种表观遗传（酵母组蛋白修饰、6 物种 4mC）。另有 GTEx v8 全血基因表达（610 受试者 × 21,004 基因，TSS±3kb≈6kb 含个体变异的双等位序列；长序列版 TSS±98K，768 基因）、变异效应（Genomics Long-Range Benchmark 致病/常见 SNP，6kb 与 196,608 bp 两版；Borzoi 来源的精细定位因果 QTL：1,896 eQTL / 540 sQTL / 116 ipaQTL / 142 paQTL）、TAD（IMR90 细胞 top5% 边界强度 2,400 bp TAD，6kb 窗口，1,500 TAD + 1,500 背景对照）。
- **评估流程**：冻结权重生成零样本嵌入 → 三种池化（summary token / mean token / max pooling）→ 下游分类器默认随机森林（对比朴素贝叶斯、elastic-net logistic 回归；5 折 CV 调参）→ AUROC 为主指标，DeLong 检验（α=0.01，单侧）做显著性比较；基因表达用随机森林回归（对比 XGBoost），Pearson r + MSE，75:25 受试者划分，配对 Wilcoxon 检验；变异效应用 embedding(alt) − embedding(ref) 效应向量 + 随机森林，严格按染色体分组的三组嵌套交叉验证（组1: chr3,6,9,12,16,18,19,21；组2: chr2,5,11,14,17,20,22,X；组3: chr1,4,7,8,10,13,15），高维嵌入（Sei/Enformer 隐藏态）调参时移除 "sqrt" 只用 "log" 选项。
- **基线 CNN**：3 层一维卷积（64/128/256 通道）+ 池化 + 线性头，A/T/C/G/N one-hot 输入，全参数训练。
- **预训练对照实验**：在 DNABERT-2 的 135 物种（6 类群、324.9 亿碱基，约为人类基因组数据 12 倍）数据集上按原设置重训 HyenaDNA-1K，与人类基因组预训练版在 49 个任务上对比。

## 3. 关键结果与指标
- **池化方法**：mean token embedding 在 52 个二元任务中显著优于其他两种池化的数据集数为——DNABERT-2 41 个、NT-v2 42 个、HyenaDNA 35 个、Caduceus-Ph 37 个、GROVER 41 个；摘要→mean 的 AUC 平均提升：4.0%（DNABERT-2）、6.8%（NT-v2）、8.7%（HyenaDNA）、5.9%（Caduceus-Ph）、1.4%（GROVER）；模型间 AUC 跨度从 summary 池化的 0.708–0.799 收窄到 mean 池化的 0.795–0.822。
- **人类基因组分类**：多数任务五模型 AUC>0.8；DNABERT-2 剪接位点供体 0.906 / 受体 0.897 最佳；Caduceus-Ph 在 TFBS、启动子（GM12878 0.9865）等任务整体最强；foundation 模型在人类任务上普遍优于基线 CNN。
- **多物种分类**：HyenaDNA 拟南芥 TATA/NonTATA 启动子 0.961/0.955 最佳（尽管只在人类基因组上预训练）；Caduceus-Ph 与 GROVER 人-vs-线虫 0.992/0.984；细菌启动子最难（R. capsulatus 最好仅 GROVER 0.715）；该类别 foundation 模型普遍不如全参数训练的基线 CNN。
- **表观遗传**：5mC 检测 NT-v2 0.738 / Caduceus-Ph 0.783 / GROVER 0.744；E. coli 4mC 上 Caduceus-Ph 最佳 0.628；NT-v2 在 A. thaliana（0.633）、C. elegans（0.649）、D. melanogaster（0.652）4mC 领先；酵母组蛋白修饰 DNABERT-2 稳健，多模型优于 CNN；表观任务 AUC 普遍比功能区分类低 10–15%。
- **基因表达**：零样本嵌入 RF 回归平均 Pearson r 仅 0.114–0.123（6kb 输入），HyenaDNA-450K（196Kbp）0.137、Enformer 0.129；个别基因强可预测（CUTALP r>0.89，DDX11 等前 10 稳定）；RF 显著优于 XGBoost（p<0.001）。
- **变异效应**：致病 vs 常见 SNP——NT-v2 平均 AUC 0.73、Cohen's d 0.88 全场最佳，超过 Enformer（0.69/0.73）与 Sei（0.66/0.60）；QTL 任务——AlphaGenome 全胜（eQTL 0.80、sQTL 0.71、paQTL 0.75、ipaQTL 0.86），Enformer eQTL 0.77 vs 通用模型最佳 Caduceus-Ph 0.65；小样本 QTL 上若干模型 AUC 低于 0.5，对染色体划分极敏感。
- **TAD 识别**：NT-v2 注意力矩阵在 TAD 中心区无显著模式——零样本下未学到高阶染色质结构。
- **预训练数据多样性**：多物种重训 HyenaDNA 在 49 个任务中 14 个显著提升（人类 5mC AUC 0.707→0.749；人-vs-线虫 0.968→0.984），仅 3 个任务（人类增强子/开放染色质/酵母表观）保留人类基因组预训练优势。
- **运行时**：单 A100、batch=1、100 次重复；HyenaDNA 长序列扩展性最好（160K 在 <2K nt 稳定、1M 版近 500K nt 仍可），NT-v2 最慢（500M 参数，100 次约 2.5 s 但稳定），GROVER 在其 2K nt 支持范围内最快。

## 4. 数据与代码可用性
- 处理后的基准数据集：https://huggingface.co/datasets/hfeng3/dna_foundation_benchmark_dataset（基因表达基准因人类参与者隐私为受限访问，需 GTEx Protected Data Access 申请）。
- 代码：https://github.com/ChongWuLab/dna_foundation_benchmark（MIT License），Zenodo 归档 10.5281/zenodo.17349484。
- 原始数据源：GTEx v8（https://www.gtexportal.org）、Genomics Long-Range Benchmark（Hugging Face InstaDeepAI）、Borzoi QTL（Google Cloud borzoi-paper/qtl）、Basenji Hi-C TAD（basenji_hic/insulation）。

## 5. 对我们项目的可借鉴点（重点，结合大肠杆菌氨基酸细胞工厂 + AI-CRISPR 设计）
1. **DNA 基础模型嵌入可作为 gRNA 效率/活性预测的特征源（M1）**：论文给出完整可复现的"冻结零样本嵌入 + 随机森林"管线（github 代码 + HF 数据集），可直接迁移到大肠杆菌基因组上——用 DNABERT-2/NT-v2 等生成 gRNA 侧翼序列（~4–6kb，覆盖启动子/ORF 区）的嵌入，接随机森林预测切割/编辑效率，避免微调引入的偏置；大肠杆菌基因组小，嵌入生成成本极低。
2. **嵌入相减（embedding(alt) − embedding(ref)）用于变异/脱靶效应量化（M2）**：论文证明该方案可区分致病/常见 SNP（NT-v2 AUC 0.73），我们可完全复用此"参考序列嵌入 − 突变序列嵌入"框架评估 gRNA 错配靶点（on-target vs 脱靶位点分类）与编辑后氨基酸通路基因的变异效应，脱靶基准可套用其染色体分组嵌套 CV 设计（对大肠杆菌可按复制起点/基因岛分组）。
3. **池化策略是免费的性能提升**：mean token pooling 平均带来 1.4%–8.7% 的 AUC 提升且缩小模型间差异——我们在微调 gRNA 预测模型或生成全基因嵌入（如启动子活性、代谢通路基因表达预测）时默认用 mean pooling，而非 [CLS] token，并把它写进 README 的工程规范。
4. **模型选型指南**：长序列任务（>12kb，如启动子+ORF 全长、多基因操纵子）选 HyenaDNA（可到 1M nt、扩展性最好）；中等序列（≤12kb）选 NT-v2/Caduceus-Ph；若只关心局部 100–500 bp 的 gRNA 上下文，Caduceus-Ph 与 DNABERT-2 在人类功能区分类上最强，可作为大肠杆菌序列分类（启动子/TERM/RBS 识别）的底座候选；其 RC 等变性对 gRNA 双链/反义链序列天然友好。
5. **基因表达预测的现实预期**：零样本嵌入直接预测表达仅 r≈0.12，说明"gRNA 靶基因表达量"这类回归不要指望零样本嵌入一步到位——建议走微调或混合专用模型（如 Enformer 式卷积+attention）路线；论文同时给出"逐基因建模 + 受试者/菌株 75:25 划分 + 协变量回归残差化（对应其 PEER/PC 校正）"的实验设计模板，可移植到不同菌株/培养条件下的转录组数据。
6. **预训练数据多样性结论**：多物种预训练显著增强跨物种泛化——我们若要在多物种（大肠杆菌 + 其他底盘）上做 gRNA 设计，应优先选多物种预训练的 DNABERT-2/NT-v2，而非人类专属模型；若需自训底座，预训练数据要包含多样物种与 GC 差异大的基因组（大肠杆菌 50.8% GC 与人类差异大，BPE/6-mer 分词行为不同，建议做分词适配测试）。
7. **评估方法论模板**：DeLong 检验比较 AUROC、随机森林避免分类器调参偏置、"统一嵌入 + 简单分类器"的无偏基准框架可直接用于我们项目内部对不同 gRNA 模型/特征集的横向评测（M3/B2），保证结论可归因于特征而非分类器。

## 6. 与我们方案的冲突/差异点
- 论文全部基准基于人类/多物种真核基因组（GTEx、ENCODE、人类细胞系），无大肠杆菌 gRNA 活性数据；其结论（如 Caduceus-Ph 最强、mean pooling 最优）在细菌启动子任务上已出现反转（foundation 模型普遍输给任务专用 CNN，R. capsulatus 仅 0.715），说明不可直接外推——大肠杆菌上仍需自测基线 CNN vs foundation 嵌入。
- 论文强调"零样本 + 冻结权重"评估以消除微调偏置，而我们的 gRNA 效率预测通常需要微调/全参数训练，两者目标不同：其结论用于模型选型与特征提取，不宜当作"微调后也如此"的证据。
- 其变异效应框架针对单核苷酸变异（SNP/QTL），gRNA 脱靶是 18–23 nt 的插入/错配/缺失模式，效应向量维度与噪声特性不同，需改造（如按位错配掩码嵌入）而非直接套用。

## 7. 行动项建议
- 纳入 README 模型选型章节：gRNA 上下文嵌入底座默认 DNABERT-2/NT-v2（多物种预训练），长序列任务用 HyenaDNA；记录"mean pooling 优先"工程规范。
- 复现基线：用其 github 代码在 E. coli 数据集（如 4mC、启动子分类）上做一次 5 模型 × 3 池化的零样本基准，验证其结论在细菌上的可迁移性，结果写入 B2 管线文档。
- 借鉴 M2：实现 gRNA 脱靶评分的"参考嵌入 − 错配靶点嵌入"特征，与现有序列比对得分（MM 数、PAM 相容性）融合进脱靶模型。
- 基因表达模块：以"协变量回归残差 + 随机森林/微调模型"实验模板，处理我们多菌株 β-丙氨酸/L-高丝氨酸转录组数据。
- 数据入库：HF 数据集（尤其 E. coli 4mC）可作为甲基化/调控区识别辅助训练集。
