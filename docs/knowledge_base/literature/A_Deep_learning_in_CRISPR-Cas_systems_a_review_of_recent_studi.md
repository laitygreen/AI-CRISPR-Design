# 文献卡：Deep learning in CRISPR-Cas systems: a review of recent studies

| 字段 | 内容 |
|---|---|
| 分级 | A |
| 主题 | T1 gRNA效率（并覆盖编辑结果预测、高活性 gRNA 设计、自动化系统、新兴应用，属领域综述） |
| 年份 | 2023 |
| 期刊 | Frontiers in Bioengineering and Biotechnology |
| DOI | 10.3389/fbioe.2023.1226182 |
| 项目映射 | M1、M2、M4（综述支撑：gRNA 活性预测、编辑结果预测、物种特异模型与自动化/大模型趋势） |

> 注：M1–M4/B1–B3/D 模块编号按项目背景（gRNA效率预测、脱靶评估、细胞工厂设计、LLM/Agent、基础支撑）推断映射。

## 1. 一句话核心
对 2019–2023 年（Web of Science 检索、54 篇同行评审论文）深度学习在 CRISPR-Cas 系统中的应用做系统综述，按"gRNA 活性预测 / 编辑结果预测 / 高活性 gRNA 设计 / 自动化系统 / 新兴话题（anti-CRISPR、核酸检测、Cas 变体、公众舆情）"五类梳理；指出 CNN 主导、BiLSTM/混合模型/注意力机制兴起、物种特异模型必要，以及"各研究使用独立数据集与不同指标、缺乏统一基准导致无法数值比较"的领域性挑战。

## 2. 方法要点（详细）
- **文献选择流程**：WoS 数据库检索，关键词"deep learning"+"CRISPR-Cas"+"neural network"；仅收录同行评审期刊论文（排除综述/观点/预印本）；时间窗 2019–2023（2023 年数据截至 5 月）；最终 54 篇。
- **量化统计**：中位引用 7、平均引用 16.1；年度分布 2019:8 篇、2020:10 篇、2021:17 篇（2022/2023 数据持续增长）；期刊分布：BMC Bioinformatics、Computational and Structural Biotechnology Journal、Nature Communications 各 4 篇（各约 7.4%），Nucleic Acids Research、Bioinformatics 各 3 篇，其余 51.8% 分散于 Misc.
- **五类主题与代表工作**：
  1. gRNA 活性预测（26 项）：Ameen 2021 CNN-SVR（Cas12）；Shrawgi DeepSgRNA（CNN）；Dimauro CRISPRLearner；Xie CRISPR-OTE（CNN+biLSTM）；Xue DeepCas9；Wan TransCrispr（Transformer+CNN）；Zhang CNN-SVR；Li CNN-XG（CNN+XGBoost）；Xiang CRISPRon；Kirillov 2022（Capsule Network+Gaussian Process，不确定性+可解释）；Elkayam DeepCRISTL（BLSTM+迁移学习）；Niu R-CRISPR（off-target）；Luo DeepCpf1；Zhang CRISPR-ONT/OFFT（注意力 CNN）；Yang EpiCas-DL（表观编辑 sgRNA 设计）；Zhang DL-CRISPR；Liu CnnCrispr；Zhang CRISPR-IP（CNN+BiLSTM+attention）；Charlier 2021（8×23 编码）；Lin 2022（CNN+自注意力）；Niu sgRNACNN（4 种作物集成 CNN）；Jost 2020（CRISPRi 滴度调控规则）；Xiao AttCRISPR；Wang & Zhang 2019（大肠杆菌 E. coli 物种特异 CNN）。
  2. 编辑结果预测：CROTON（多任务 CNN＋神经架构搜索 NAS，自动化特征与模型工程）；Apindel（BiLSTM+attention，预测 Cas9 突变结局）；EditPredict（CNN，RNA 编辑/ADAR1 敲除预测）；SeqGAN（CNN+GAN，off-target 切割位点）；Naert 2020/2021（爪蟾/斑马鱼 F0 表型外显率提升；CRISPR-SID 肿瘤基因依赖）；BE-DICT（attention，碱基编辑结局）；Zhang 2021b（SpRY off-target 验证与 Cas9 变体评估）。
  3. 高活性 gRNA 设计：DeepGuide（Yarrowia lipolytica 基因组活性筛选，Cas9/Cas12a，显著提升突变成功率）；DeepHF（RNN+生物学特征，高保真 SpCas9 变体）；Feng 2021（dCas9-sgRNA 错配生物物理模型+CNN，细菌 CRISPRi）；Kim 2020a（xCas9/SpCas9-NG 活性预测、非 NGG PAM 评估）。
  4. 自动化系统：斑马鱼胚胎自动注射（Inception-v3 图像识别）；流式成像平台（CRISPR/AAV 诱导 DNA 损伤应答表型筛选）；单细胞电穿孔平台（FCN 定位核/胞质+递送 gRNA 复合物至 iPSC）；AI-PS（CNN+CRISPRi 池化筛选，光激活分离目标细胞）。
  5. 新兴话题：RAVI-CRISPR（Cas12a+CNN 比色检测 SARS-CoV-2/ASFV）；HDAC 活性直接检测；Cas12a/Cas13a 外泌体蛋白同步检测；anti-CRISPR 蛋白识别（Wandera 2022）；AcrIIA4 功能工程；AlphaFold2 anti-CRISPR 结构预测；13 种 SpCas9 变体活性预测（Kim N. 2020）；BPNet（转录因子结合）；Twitter 舆情分析（Muller 2020）。
- **趋势总结**：CNN 最常用（局部模式识别、位置鲁棒）；BiLSTM 捕获长程依赖；混合模型（CNN+SVR/XGBoost/注意力/GAN）兴起；注意力机制提升可解释性；物种特异模型（细菌 vs 人）受重视；可解释性与可复现性成关注点。

## 3. 关键结果与指标
- 综述层面：54 篇论文的分布与趋势（2021 年 17 篇爆发、中位引用 7）；领域内"无统一数据集与指标（log-likelihood/AUC/accuracy/cosine similarity/embedding 各异），数值横向比较 virtually unfeasible"是核心挑战。
- 代表性成果（转述）：DeepGuide 显著提升 Yarrowia lipolytica 的 CRISPR 突变成功率；DeepHF 优于同期模型与设计工具；BE-DICT 碱基编辑结局预测高精度；EditPredict RNA 编辑预测高精度；CROTON 实现自动化特征+模型工程；Wang & Zhang 2019 大肠杆菌 sgRNA CNN（Spearman 0.582/0.7105/0.360，被引作物种特异必要性证据）；Naert 2020 用预测建模显著提高 F0 表型外显率。

## 4. 数据与代码可用性
- 综述未提供统一数据集或代码；各引用论文的数据/代码见原文参考文献（如 DeepHF、CRISPRon、DeepGuide、DeepCRISTL、CRISPR-IP 等原始论文）。

## 5. 对我们项目的可借鉴点
1. **物种特异模型是硬需求**：综述点名 Wang & Zhang 2019 的 E. coli sgRNA 模型与 sgRNACNN（4 作物），证实"人源模型直接迁移到细菌不可行"——我们 M1 必须用 E. coli 自身数据训练，人源数据只能做预训练/辅助。
2. **编辑结果预测进设计闭环**：Apindel/BE-DICT/CROTON 提示可增加"预测敲除/编辑结局（indel 分布、移码概率）"子模块；对 E. coli 基因敲除，可评估同义/移码突变效果，服务 β-丙氨酸/L-高丝氨酸细胞工厂的基因改造设计（M3 联动）。
3. **混合架构候选**：CNN+BiLSTM+attention（CRISPR-IP）、Transformer+CNN（TransCrispr）、CNN+胶囊网络+GP（不确定性）是目前性能/可解释平衡较好的范式，作为我们 M1 主模型候选架构。
4. **自动化/高通量闭环**：综述第 6 节（自动注射、单细胞电穿孔、池化筛选+DL 图像分析）提示"AI-CRISPR 系统"应包含实验自动化环节——我们可设计"sgRNA 设计→文库合成→高通量筛选→活性回灌训练"闭环，让模型持续迭代。
5. **不确定性量化**：Kirillov 的 capsule+GP 给每个 gRNA 预测附带置信区间，可驱动"低置信度 gRNA 优先湿实验验证"的主动学习，契合我们实验资源有限的约束。
6. **新方向扫描**：anti-CRISPR 识别、Cas 变体活性（xCas9/SpCas9-NG/SpRY）预测、Cas12a 检测等为后续模块扩展（如 Cas12a 变体、递送设计）提供素材。

## 6. 与我们方案的冲突/差异点
- 综述覆盖以人源/真核为主，E. coli 内容占比小，对原核 sgRNA 设计的具体参数指导有限。
- 综述明确指出无统一数据集与指标，其数值不可直接引用为对比结论；必须在我们自己的统一协议下重测。
- 部分主题（舆情分析、核酸诊断）与代谢工程目标关联弱，借鉴时应聚焦 gRNA 活性预测与编辑结果预测两类。

## 7. 行动项建议
- 用综述的论文清单补全文献库（DeepHF、DeepCRISTL、CRISPR-IP、TransCrispr、EpiCas-DL、DeepGuide、Apindel 等），逐篇出文献卡。
- 将"统一评测协议（去泄漏划分、统一指标、简单基线对照）"列为 B2 模块的硬性要求，写入项目规范。
- 在 README 记录：物种特异模型必要性＋主动学习/不确定性闭环的设计依据。
