---
# 文献卡：CRISPR genome editing using computational approaches: A survey

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T1 gRNA效率 + T2 脱靶 |
| 年份 | 2023 |
| 期刊 | Frontiers in Bioinformatics（Front. Bioinform. 2:1001131） |
| DOI | 10.3389/fbinf.2022.1001131 |
| 项目映射 | M1、M2、B2、D |

> 模块约定：M1=gRNA设计与效率预测；M2=脱靶评估；M3=LLM与Agent；M4=细胞工厂设计；B1=数据层；B2=模型层（算法/模型库）；B3=生信管线平台；D=知识库/README。

## 1. 一句话核心
系统性综述 CRISPR gRNA 设计与脱靶预测的计算方法（传统机器学习 + 深度学习），对比了 30+ 个工具，指出以 CNN 为主的深度学习方法是未来最有效方向，但其精度高度依赖训练数据规模与输入编码方式（one-hot 是当前瓶颈），并给出"错配数越多脱靶活性越低（1 错配约 59% → 4 错配趋近 0%）"等关键经验规律。

## 2. 方法要点（详细）
- **问题框架**：gRNA 设计两大目标——高 on-target 活性 + 低 off-target 效应；SpCas9 PAM 为 NGG（人基因组中"GG"频率 5.21%，约每 42 bp 一个 NGG，全基因组约 161,284,793 个位点），切割发生在 PAM 上游 3 bp。
- **工具分类体系**（文中 Table 1–4）：① CRISPR 系统基础工具（CRISPRidentify、CRISPRloci、ANNOgesic、CRISPR-DAV 等，用于阵列检测/注释）；② 脱靶查找工具（Table 2）；③ gRNA 设计工具（Table 3）；④ 机器/深度学习（MDL）工具（Table 4）。
- **脱靶预测两类方法**：
  - **比对法（alignment-based）**：BLAST/Bowtie/BWA 或暴力搜索（brute force）引擎。代表：Cas-OFFinder（GPU 加速、不限制错配数与 PAM 类型、支持 1 bp 缺失/插入，综合评价最高）；CCTop（把 Bowtie 默认 1 错配改为最多 5 错配检索 protospacer）；CRISPRitz（4-bit 核苷酸编码 + 位运算，支持错配与 indel）；CALITAS（CRISPR 调优的 Needleman–Wunsch，无限错配/gap，支持 PAM 错配或 PAM-less 搜索）；OffScan（FM-index，提速降内存）；FlashFry、CRISPR-SE（暴力搜索，速度快）。
  - **打分法（scoring-based）**：MIT score（Hsu 2013，错配位置权重矩阵）；CFD（加入非经典 PAM NAG/NCG/NGA，GUIDE-seq 验证优于 MIT）；CRISPRoff / uCRISPR（叠加能量特征，精度优于 MIT/CFD）。
- **ML/DL 效率预测模型**：Rule Set 1（SVM+线性回归）、Rule Set 2（统计核苷酸在基因内位置，适用于 KO 与 CRISPRa/i）、sgRNA Designer / Elastic Net（Broad Institute）、SSC（Elastic Net）、CRISPRscan（逻辑回归，加入 G 富集/A 缺失特征）、WU-CRISPR（SVM）、SgRNAScorer（SVM，支持 SaCas9/AsCpf1）；DL：DeepCRISPR（CNN，on-target+全基因组 off-target 联合预测）、DeepHF、DeepSpCas9、DeepCpf1（CNN+染色质可及性数据）、C-RNNCrispr（CNN+BGRU，大数据集预训练后用小数据集迁移微调）、Deeper-Bind（LSTM 建模序列依赖）。
- **评估协议**：Accuracy / Precision / Sensitivity 公式（TP/FP/TN/FN）+ Spearman 相关系数（SCC，跨数据集比较的推荐指标）；跨 5 个数据集（Zebrafish_G、Zebrafish_S、HEL、A375、mESC）做"工具×数据集"多边形稳健性比较；深度学习工具按不同基因组/细胞系精度差异大（如 DeepCRISPR 在 HEL 最准、其余数据集表现差）。
- **CRISPOR 工具**：含 417 个基因组、19 种 PAM；输出 2 个特异性分数（MIT、CFD）+ 10 个效率分数（Rule Set 2、CRISPRscan、microhomology、Lindel 等），并为每个 gRNA 与脱靶位点设计验证引物。
- **现存挑战**（结论部分明确列出）：数据不平衡、数据异质性、训练数据不足、泛化性差、跨物种失效；暗区（AT/GC-rich、重复低复杂度区）预测困难，需无扩增长读测序（SMRT/Nano-OTS）补充训练数据。

## 3. 关键结果与指标
- 脱靶活性随错配数衰减：1 个错配时约 59%，4 个及以上趋近 0%。
- 跨 5 数据集稳健性：DeepHF、DeepSpCas9、DeepCas9 多边形面积最大（最稳健）；经典 ML 的 Azimuth 2.0 与 DL 相当；E-CRISP 精度不错但相关性（SCC）不高、胜在跨数据集稳定；DeepCRISPR 在 HEL 数据集最佳。
- 综述结论：DL 方法精度取决于可用训练数据量；gRNA-DNA 配对编码、新的 embedding/编码方式（替代 one-hot）可进一步提升现有 DL 架构。

## 4. 数据与代码可用性
综述本身无自有数据集/代码（未提供）。但文中列出全部工具的访问链接，均可免费使用：Cas-OFFinder（rgenome.net/cas-offinder）、CRISPOR（crispor.org）、CHOPCHOP（chopchop.cbu.uib.no）、FlashFry、CCTop、CRISPRitz（GitHub）、DeepCRISPR（deepcrispr.net）、DeepHF（deepHF.com）、DeepSpCas9（deepcrispr.info）、CRISPR-SE、CALITAS（GitHub: editasmedicine/calitas）等。

## 5. 对我们项目的可借鉴点（重点，结合大肠杆菌氨基酸细胞工厂 + AI-CRISPR 设计）
1. **直接作为 M1/M2 基线工具库**：把 Table 2/3/4 中的 Cas-OFFinder、CRISPOR、CHOPCHOP、DeepSpCas9、DeepHF、C-RNNCrispr 作为我们在 E. coli K-12 MG1655 基因组上 gRNA 效率与脱靶预测的对比基线，统一评测后写入 README。
2. **效率特征清单**：文中归纳影响切割效率的三类特征——序列组成（位置核苷酸偏好、GC 含量）、遗传/表观遗传（染色质可及性、基因表达）、能量性质（RNA 二级结构、解链温度、自由能）；为 E. coli gRNA 效率模型提供可直接落地的特征工程清单（原核无染色质维度，可替换为转录活性/甲基化数据）。
3. **评估协议借鉴**：用 Spearman 相关而非 MSE 比较模型；按"工具×数据集"稳健性分析（多边形图）报告跨菌株/培养条件的稳定性，避免单数据集过拟合结论。
4. **小样本训练策略**：C-RNNCrispr 的"大模型预训练 + 小数据集迁移微调"直接对应我们 gRNA 效率标注数据稀少的问题；可先用人/哺乳动物大 gRNA 数据集预训练，再用 E. coli 少量实测数据微调。
5. **编码升级方向**：综述明确指出 one-hot 是 DL 方法瓶颈、建议 gRNA-DNA 配对编码与新型 embedding——与我们的 LLM 序列嵌入（DNABERT 类）路线一致，可作为 M3 与 M1 衔接的设计依据。
6. **"错配→活性"先验**：把 59%（1 错配）→0%（4 错配）的衰减规律作为 M2 脱靶打分的先验/正则，指导 E. coli 基因组脱靶位点筛选的错配容忍阈值（建议 ≤3 错配）。

## 6. 与我们方案的冲突/差异点
- 文中几乎所有工具与评测数据面向人/小鼠基因组（HEL、A375、mESC、Zebrafish），缺少原核/大肠杆菌数据；直接套用模型权重需重新训练，评测指标不能直接引用。
- 综述倾向"多工具交叉验证、用户自己挑"，而我们的系统需要端到端可部署的单一 pipeline，需做工具裁剪与统一接口封装。
- 综述结论基于 2018–2021 年的模型，未覆盖 DNABERT-S、Nucleotide Transformer、Generanno 等新 LLM 时代工作，需用更新文献（本批 DCVBin/Generanno 卡）补充。

## 7. 行动项建议
- 写入 README：建立 M1/M2 基线工具表（工具名、链接、输入输出格式、适用基因组、许可）。
- 复现基线：在 E. coli K-12 上运行 Cas-OFFinder 与 CRISPOR 做脱靶评测；用公开 gRNA 数据集复现 DeepSpCas9 / DeepHF 作为 M1 效率预测基线。
- 采用 SCC + 多数据集稳健性报告模板作为 B3 评估规范。
- 将"错配数→脱靶活性衰减"先验纳入 M2 打分模块。
- 调研 C-RNNCrispr 迁移学习代码（GitHub: Peppags/C_RNNCrispr）作为小样本 gRNA 数据训练的起点。
