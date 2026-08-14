# 文献卡：Novel CRISPR-Cas12a Clades Discovery Using Large Language Model

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T1 gRNA效率（兼 T2 脱靶、T3 DNA底座） |
| 年份 | 2024（Research Square 预印本 2024-08-06）；正式发表版 2025（Nature Communications，2025-08-23） |
| 期刊 | Nature Communications（正式版；预印本 Research Square） |
| DOI | 10.1038/s41467-025-63160-4（正式版）；预印本 10.21203/rs.3.rs-4817511/v1 |
| 项目映射 | M1（基于 ESM 嵌入 + 小样本 ML 的切割活性预测）、M2（PAM 偏好与错配/脱靶分析）、M3（ESM 蛋白语言模型底座）、B2（宏基因组挖掘与 Cas 注释管线） |

## 1. 一句话核心
提出 AIL-Scan 策略：用 ESM-2 蛋白语言模型（650M/15B 参数）微调后对 CRISPR-Cas 蛋白做无序列比对的精准分类（77,684 条 Cas 序列，98.22% 准确率），并在宏基因组中发现 7 个新型 Cas12a 亚型（按 CRISPR 位点整合酶 Cas1/Cas2/Cas4 组合定义 8 类），通过"ESM 嵌入 + PCA + 小样本机器学习"预测新 Cas12a 的反式切割活性（92.3% 准确率），再经生化与冷冻电镜（AmCas12a-crRNA，2.9 Å）表征出不同的 PAM 偏好（含 G 起始宽 PAM 的 AmCas12a）、切割偏好与错配耐受，最终实现无需传统 TTTV PAM 的 KRAS G12C 单核苷酸突变检测（灵敏度 0.1%）。

## 2. 方法要点（详细）
- **AIL-Scan 三步**：① 构建 CRISPR-Cas 训练数据（NCBI reviewed 基因注释，标注 Cas1–Cas13 共 12 类；非 Cas 蛋白规则=无 cas 注释且与已知序列相似度 <40%；CD-HIT-2D 40% 同源性阈值去冗余并划分训练/验证集）；② 监督微调 ESM-2（650M 与 15B）做多标签 Cas 蛋白分类；③ 特征预测（切割活性、CRISPR 位点类型/长度、直接重复、间隔序列、进化分析、MSA、结构）。
- **训练细节**：数据量 77,684 条非冗余正样本（Cas1 11,248 / Cas2 15,148 / Cas3 12,309 / Cas4 7,708 / Cas5 8,656 / Cas6 11,281 / Cas7 340 / Cas8 299 / Cas9 6,706 / Cas10 3,525 / Cas12 334 / Cas13 130）+ 13,047 条非 Cas，最长 1,764 aa；80/20 划分；分类头=两层全连接（线性→Tanh→线性）；Focal Loss 处理类别不平衡（超参 α 按类别比例设定）；AdamW + WarmupLR；DeepSpeed ZeRO-3 offload；PyTorch；A100 GPU。
- **宏基因组挖掘**：GMGC 数据库选 50,000 个高质量 bin、提取含 CRISPR 位点的 20,000 个 MAGs；Prodigal 预测基因；约 2,000 万条 <1,500 aa 蛋白序列输入 AIL-Scan → 预测出 1,379 条 Cas12a 序列。
- **反式切割活性预测（小样本问题解法）**：69 条有标签 Cas12a（33 条 active / 36 条 inactive；FQ 荧光报告实验，活性定义为荧光 ≥2× 阴性对照；含 3 个已知 Cas12a）；13 条测试（约 20%）/ 56 条训练；取微调后 ESM 最后一层 1,280 维嵌入作协变量；先直接喂 LightGBM（69.2%），再 PCA 降维（2–15 主成分）——LightGBM+PCA-6、CatBoost+PCA-4、RandomForest+PCA-8 均达 92.3%（13 条中 12 条正确）。
- **亚型与结构分析**：手工验证 300 个预测 CRISPR 位点（另用 1,000 个未验证位点交叉确认分布一致）；按整合酶组合分 8 亚型（I=Cas1+Cas2+Cas4 … VIII=无整合酶，VI 仅 Cas2）；位点长度从第 VIII 型 4,200 bp 到第 I 型 6,100+ bp（个别 6,700 bp）；间隔子数在 IV/VI/VIII 型显著减少；直接重复的茎环区保守。Cas1（92–331 aa）、Cas2（70–146 aa）、Cas4（79–206 aa）各用 AlphaFold2 建模 + 成对结构比对分出 8 个结构型（如 Cas4 缺失 β5/β6 破坏间隔子插入方向性）。
- **生化表征**（16 个新 Cas12a，来自 8 亚型：AmCas12a、EvCas12a_1/2、EspCas12a、RspCas12a_1/2、ArCas12a、LeCas12a_1/2、UBACas12a、RCCas12a、CAGCas12a、RbrCas12a_1–4；与已知 Cas12a 序列一致性仅 30–46%）：
  - PAM 检测：每孔退火 256 种 PAM 引物对构建 6 个 dsDNA 靶阵列（EMX1 site1、DNMT1 site1、FANCF site1、MerS site1、eGFP site1/site3），FAM-BHQ 荧光报告；EvCas12a_2/RspCas12a_2/CAGCas12a 偏好 T 富集 PAM，AmCas12a 偏好 G 起始（更宽），RbrCas12a_1 识别 5'-GTV-3'。
  - 顺式/反式切割：37°C 下除 RCCas12a 外均能以接近 LbCas12a 的效率切割线性化 dsDNA；室温下多数活性下降、第 VIII 型（无整合酶）例外；二价离子偏好——低活性变体 Mg²⁺ 无法激活反式切割，Mn²⁺ 可激活（Co²⁺ 对 RspCas12a_2 更好）。
  - HEK293T 基因组编辑效率（6 个典型 PAM 位点）：AmCas12a 平均 49.6%（位点 3 达 85.4%、位点 6 达 84.9%）、ArCas12a 45.4%、CAGCas12a 28.8%（位点 4 峰值 81.7%）、EvCas12a_2 20.3%、RbrCas12a_2 17.8%、RspCas12a_2 14.3%、LeCas12a_1 6.2%、UBACas12a 近 0（最高 2.1%）；对照 AsCpf1 65.5%、LbCas12a 25.6%。
  - 错配耐受（脱靶相关）：seed 区单碱基错配几乎完全抑制切割，PAM 远端错配大多耐受（与已知 Cas12a 一致）。
- **结构解析**：AmCas12a-crRNA（44-nt crRNA）复合物冷冻电镜 2.9 Å（PDB 8KGF / EMDB EMD-37219）；发现 crRNA spacer 区额外 RNA 茎（A(1)–A(5) 与 U(18)–U(22)），使 seed 区清晰；REC 结构域相对 Lb/FnCas12a 旋转（REC1 偏离 7.3°/9.4°，REC2 4.8°/6.2°）；spacer 主要与 WED 结构域互作（关键残基 T19、H751、K522、H861、Y50、R168、Q1003）。
- **SNP 检测应用**：KRAS c.34G>T（G12C）旁无传统 TTTV PAM；按 AmCas12a PAM 偏好设计 crRNA；RPA 扩增 + Cas12a 荧光检测，检出下限 10 拷贝，可在野生型背景中区分 0.1% 突变（优于 Sanger 测序）。

## 3. 关键结果与指标
- **Cas 分类**：ESM-2 650M 第 13 epoch 准确率 97.75%，15B 第 9 epoch 98.22%；逐类准确率（650M/15B）——cas9 100%/100%、cas12 100%/100%、cas13 100%/100%、non-Cas 99.8%/99.9%、cas1 98.5%/98.5%、cas4 89.9%/94.4%、cas8 88.9%/100%；小蛋白（Cas1/2/3/4/5/8）预测更难，15B 提升显著；与 CRISPRcasIdentifier（HMM+ML）相当、优于 HMMCAS 与 CASPredict（SVM，最快但最不准）。
- **反式切割活性预测**：嵌入直训 LightGBM 69.2% → PCA 降维后 CatBoost+PCA-4 / LightGBM+PCA-6 / RandomForest+PCA-8 各 92.3%（12/13）。
- **新亚型发现**：7 个新 Cas12a 亚型（+1 已知型=8 类）；94.6% 来自肠道微生物；Lachnospiraceae 232 条聚为一支（Subclade 1 含 62 条 I 型 + 81 条 VII 型；Subclade 3 为 Acutalibacteraceae 28 条 VIII 型）。
- **功能验证**：AmCas12a 平均编辑效率 49.6%（最高位点 85.4%），接近 AsCpf1（65.5%）；KRAS G12C 检测灵敏度 10 拷贝 / 0.1% 突变比例。
- **结构**：2.9 Å cryo-EM 结构 + AlphaFold2 300 个 Cas12a 结构模型 + 三类整合酶各 8 结构型。

## 4. 数据与代码可用性
- 代码：https://github.com/LUCA-BioTech/cas_classification。
- 数据：深度测序数据 NCBI PRJNA1043844；结构 PDB 8KGF、EMDB EMD-37219；其余材料可向通讯作者索取。

## 5. 对我们项目的可借鉴点（重点，结合大肠杆菌氨基酸细胞工厂 + AI-CRISPR 设计）
1. **"蛋白语言模型嵌入 + 小样本 ML"预测切割活性（M1 直接复用）**：其用微调 ESM 的 1,280 维嵌入 + PCA + 树模型在仅 69 个样本上把 Cas12a 反式切割活性预测做到 92.3%（12/13）——我们训练大肠杆菌 gRNA 效率模型时，若实验数据少（如几百条），可完全照搬"预训练嵌入（ESM/Prottrans/DNABERT-2）→ PCA 降维到 4–8 维 → LightGBM/CatBoost/RandomForest"配方；其"直接训练 69.2% vs PCA 后 92.3%"的对比是"小样本先降维"的有力证据。
2. **类别不平衡与正负样本定义（M1 训练技巧）**：active 定义为荧光 ≥2× 阴性对照；Focal Loss 处理类别不平衡、超参 α 按类别比例设置——我们定义"高效/低效 gRNA"标签时可采用同样阈值化与 Focal Loss 策略。
3. **PAM 识别与宽 PAM 变体拓宽设计空间（M2/T1 特征）**：AmCas12a 识别 G 起始宽 PAM、RbrCas12a_1 识别 5'-GTV-3'——若我们在大肠杆菌中除 Cas9（NGG）外引入 Cas12a 编辑器，宽 PAM 变体可显著扩大可靶向位点（尤其 AT 富集的氨基酸生物合成启动子区）；其 256 种 PAM 阵列检测法是标准化的 PAM 偏好测定流程，可直接用于评估我们体系。
4. **错配耐受规律用于脱靶建模（M2）**：seed 区错配几乎完全抑制、PAM 远端错配耐受——这是 Cas12a 脱靶评分的先验权重（seed 区错配惩罚高、远端惩罚低），可直接融入我们的脱靶评估模块（对 Cas9 则 seed 区 PAM 近端规则类似）；其"深度测序 + BWA-MEM + indel 频率=含 indel 读数/总比对读数"是编辑效率评估的完整实验管线，可复刻为我们的湿实验验证协议。
5. **宏基因组挖掘管线（B2 扩展）**：GMGC bin → Prodigal 基因预测 → ESM 分类 → 位点结构分析（CRISPRCasTyper 式）——若项目需要挖掘新型 Cas 变体（如更适合大肠杆菌的紧凑编辑器），AIL-Scan 是现成模板；其"小 Cas 蛋白（Cas1/2/4/8）短序列难预测、增大模型显著提升"的结论指导我们在短序列任务上优先更大模型。
6. **结构-功能闭环验证范式**：AlphaFold2 300 个结构 + cryo-EM 验证 + 生化活性 + 编辑效率 + SNP 检测，形成"预测→结构→功能→应用"完整证据链——我们项目的 XAI/预测模块可借鉴此验证层级（预测靶点 → 结构/序列分析 → 实验验证）。
7. **RPA+Cas12a 检测系统（应用拓展）**：10 拷贝/0.1% 灵敏度的等温扩增检测，可作为大肠杆菌发酵产物（β-丙氨酸/L-高丝氨酸）快速检测或工程菌株突变检测的应用展示。

## 6. 与我们方案的冲突/差异点
- 论文预测对象是 Cas12a 蛋白的反式切割活性（蛋白层面，69 个样本），我们预测的是 gRNA 的编辑效率/脱靶（核酸层面、样本量大得多）——方法（嵌入+PCA+树模型）可迁移，但特征空间与任务定义不同，需重新训练与验证。
- 其错配耐受结论基于 Cas12a（seed 区在 PAM 远端、crRNA 长 spacer），与我们主要使用的 Cas9（seed 区在 PAM 近端）规则不同，脱靶先验不能照抄，需按酶型分别建模。
- 该研究面向人源基因编辑/分子诊断（HEK293T、KRAS 癌基因），我们面向大肠杆菌代谢工程，其 PAM/编辑效率数值不能直接外推到细菌宿主（细菌无真核修复背景、无 NHEJ 主导修复），需在 E. coli 中自测。
- 预印本与正式版数据细节有出入（摘要写 7 亚型、正文 8 类），引用时以正式版 Nature Communications 为准。

## 7. 行动项建议
- 复现基线（M1）：在自有 gRNA 效率小数据集上实现"ESM/DNA 基础模型嵌入 → PCA(4–8) → LightGBM/CatBoost/RF"配方，与现有 gRNA 模型对比，验证小样本场景的增益。
- 纳入训练集：其 69 条 Cas12a 活性标签（Table S1）与 PAM 数据可作蛋白层面活性预测的辅助训练/验证集；代码仓库 cas_classification 可作 Cas 注释基线。
- 改进 M2：把"seed 错配强惩罚、PAM 远端弱惩罚"写入脱靶评分规则（Cas12a 版），并在 README 记录与 Cas9 规则的差异。
- 实验设计参考：采用其编辑效率评估协议（靶向深度测序 + indel 频率）与 PAM 阵列检测法，作为我们大肠杆菌 gRNA 湿实验验证的标准流程。
- 写入 README：记录"小样本先 PCA 降维再树模型""Focal Loss 处理不平衡""小蛋白短序列需大模型"三条方法论经验。
