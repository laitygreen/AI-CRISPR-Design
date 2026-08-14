---
# 文献卡：Interpretable prediction of DNA replication origins in S. cerevisiae using DNABERT and DNABERT-2

| 字段 | 内容 |
|---|---|
| 分级 | A |
| 主题 | T4 LLM与Agent（DNA 语言模型微调） + T6 生信管线（可解释性/XAI 管线） |
| 年份 | 2026（在线 2025–2026；Received 2025-11-10 / Accepted 2026-07-14） |
| 期刊 | BMC Bioinformatics, 27:157 |
| DOI | 10.1186/s12859-026-06562-5 |
| 项目映射 | M1（gRNA 效率预测：微调 + 可解释性方法论直接迁移）；M4（DNA 语言模型应用）；B2（可解释性/评估管线：注意力-motif、SHAP、混淆控制、防泄漏划分） |

## 1. 一句话核心
在酿酒酵母复制起点（ORI）预测任务上微调两个预训练 DNA 语言模型（DNABERT 与 DNABERT-2），证明二者都能学习到与已知 ARS 共识序列（ACS）一致的生物学信号但学习策略不同，并构建了"受控负样本设计 + 注意力引导的 motif 发现（attention→MEME）+ 扰动实验 + TransSHAP"的完整可解释性框架，同时发现 tokenization 策略（重叠 k-mer vs BPE）深刻影响模型的注意力行为与可解释性。

## 2. 方法要点（详细）
- **模型**：DNABERT（约 86M 参数，重叠 k-mer 分词，人类基因组预训练，BERT 12 层/768 hidden）；DNABERT-2（约 117M 参数，BPE 分词 vocab 4,096，ALiBi + Flash Attention，多物种（人/小鼠/酵母/病毒）预训练，12 层/768 hidden）。分类头：[CLS] 最后一层隐藏表示 + 全连接 + softmax；BCE 损失；全参数微调。
- **数据集设计（酵母）**：325 个 OriDB 确认 ORI（≤500 bp，用真实基因组侧翼序列不对称随机延长到 500 bp，避免位置偏差）；两个难度不同的平衡数据集共享同一正集：**Random-Neg**（325 个随机非 ORI 基因组区段）与 **ACS-Neg**（负样本必须含至少 1 个 HOMER 检出的非复制 ACS motif，17-bp 矩阵 WWW-WTTTAYRTTTW-GTT；正负 MotifScore 匹配：11.7 vs 11.5，Mann-Whitney p=0.387 / KS p=0.514 无显著差异；Random-Neg 负样本 MotifScore 仅 6.6，p<1e-43）。
- **训练**：7 次随机划分（70/10/20）；最多 200 epochs；按验证集 max(accuracy+AUC) 选最早 checkpoint；报告 7 次均值±SD。DNABERT：AdamW、lr 2e-4、warmup 0.1、batch 32；DNABERT-2：AdamW、wd 0.01、lr 3e-5、batch 32、max 125 tokens、50 步 warmup（采用各自原始论文推荐配置）。
- **注意力-motif 发现管线（DNABERT）**：末层 [CLS] 注意力分数 → 按 Ji et al. 策略投影到单核苷酸分辨率 → 阈值 0.1 选每个序列最多 4 个峰值（间隔 ≥10 bp）→ 取峰周围 20 bp 片段 → MEME（经典模式，EM 算法）做 motif 发现。
- **跨数据集扰动评估**：将正集序列随机打乱（Shuffled-Neg，保留碱基组成）或按 5 bp 块打乱（Block-5-Shuffled-Neg，保留局部结构），评估 Random-Neg/ACS-Neg 训练模型的泛化，判断分类依赖组成还是顺序特征。
- **DNABERT-2 可解释性**：① 扰动：从 ORI 序列中删除 ACS motif 实例后重测（AUC 变化）；BPE token 随机打乱重测；② 自定义 **AT-index**（全局 AT 比例 + AT 富集 motif 频率 + 最长连续 AT 串长度 + 交替 AT 串频率，归一化聚合）量化起源相关序列信号强度；③ **TransSHAP 适配**（对 BPE 分词 DNA 序列的 SHAP：以 Random-Neg 训练集为背景分布，扰动后经 BERT tokenizer 送入 Kernel SHAP），30 次运行取每次 top-50 token 统计出现频率与平均 Shapley 值。
- **人类扩展（K562）**：62,971 正 / 63,971 负（长度 99–11,899 bp）；构建 K562-L512（<512 bp）与 K562-LenMatch（负样本长度分布匹配正样本，37,438+37,438，8:2 划分）控制**长度混淆**；另做 7 折**染色体级分组交叉验证**（整条染色体不重叠地划分 train/val/test）防同源序列泄漏；DNABERT 微调 7 epochs。

## 3. 关键结果与指标
- **酵母性能（7 折均值±SD）**：DNABERT Random-Neg acc 0.83 (0.04) / AUC 0.90 (0.04)；ACS-Neg acc 0.72 (0.04) / AUC 0.79；DNABERT-2 Random-Neg acc 0.81 / AUC 0.82；ACS-Neg acc 0.72 / AUC 0.70。染色体级划分结果与随机划分相当（无随机划分高估）。
- 消融：从头训练（不预训练）DNABERT 0.71 / DNABERT-2 0.60；预训练未微调仅 0.37 / 0.55；打乱集 AUC≈0.5——预训练与任务微调都有贡献，且微调对 DNABERT 贡献更大。
- **Motif 发现（DNABERT，TP 高注意力片段→MEME）**：Random-Neg 测试集 'TTTTTWTTTATRTTT'（E-value 2.6e-6）、训练集 'TATATTTATRTWTWT'（E-value 2.3e-32），与实验确认的 ACS 'WTTTATRTTTW' 高度一致；ACS-Neg 训练集 'ATATATATATATDTA'（E-value 1.6e-26，交替 A/T，对应基因间起点）；TN 片段无显著 motif（负预测无单一主导模式）。
- **跨数据集扰动**：Random-Neg 训练模型在打乱集 AUC 0.68–0.69（组成差异贡献大，但仍远高于未微调基线 0.5，说明学到 ACS 等顺序信号）；ACS-Neg 训练模型 AUC 约 0.81（依赖与 ACS 不同的特征）。
- **注意力模式**：DNABERT-2 强对角注意力（局部、短程依赖，突出 [SEP] 列）；DNABERT 除对角外有非对角高注意力列（捕获全局/长程依赖）——同一序列两模型注意力模式根本不同。
- **DNABERT-2 扰动**：删除 ACS motif 仅使 10% 的正预测翻转、AUC 0.82→0.77；token 打乱后 TP 全部仍分类正确（强信号下依赖 token 身份），TN 平均减少 30%（44→26）、FP 近乎翻倍（21→39）、AUC 0.82→0.75。
- **SHAP 结果**：top 贡献 token 全部 A/T 富集（AAAAAAA、TATATATATATATA、TATATA…等，含 TATA-like 交替模式）；TP 序列 AT-index 均值 0.61，TN −0.45，TN→FP −0.17；TP vs TN：p=3.4e-14、Cliff's |δ|=0.87；TP vs TN→FP：p=2.3e-5、|δ|=0.73。
- **人类 K562**：K562-L512 acc 0.996 / AUC 0.997（但长度本身成为判别信号）；K562-LenMatch acc 0.894 / AUC 0.956（更保守、受控）；高于 Ori-FinderH（AUC 0.9616，K562-L512 对比下为 0.997）；染色体级划分性能与随机划分相当（非记忆同源序列）；注意力峰值片段发现 **G 富集 motif**（E-value 低至 1.2e-327，随注意力约束越强 G 富集越明显），与人源复制起点 G-四链体关联一致。
- 与既往方法对比（无统一基准，仅概念类比）：MEL（Singh et al.）nrACS AUC 0.76 vs 本文 ACS-Neg AUC 0.82/0.72；XGBoost（Do & Le）acc 0.89（300 bp 简单数据集）；Word2Vec+CNN（Wu et al.）acc 0.97（需大量预处理）。

## 4. 数据与代码可用性
- 酵母数据集全部在补充材料（Additional Files 2–5，CSV）；源自 OriDB：https://oridb.org。
- 代码/数据集（酵母与人）：GitHub https://github.com/Piroozeh/DNAOriginPrediction（原文写作 "github.com/Piroozeh/DNAOrigin Prediction"，应为此仓库）。
- 许可：CC BY 4.0（开放获取）；无独立训练好的模型权重发布（文中未提及）。

## 5. 对我们项目的可借鉴点（重点，结合大肠杆菌氨基酸细胞工厂 + AI-CRISPR 设计）
1. **难负样本设计（Random-Neg vs ACS-Neg 双数据集）直接迁移到 gRNA 效率预测（M1/T1）**：模拟"ACS 类似物负样本"思路——构建 (a) 随机基因组负集与 (b) 含 PAM/种子区相似但不切割或不高效的 gRNA 难负集，分别训练并对比，检验模型学到的到底是 PAM/种子匹配等简单特征还是真实效率信号；正负样本用 MotifScore 匹配统计（Mann-Whitney/KS 检验）证明"无法用简单 motif 区分"。
2. **注意力引导的 motif 发现管线（attention→20bp 片段→MEME）可作为 gRNA 模型的可解释性标准件（B2）**：用 [CLS] 注意力投影到单碱基 + 阈值 0.1 选峰 + MEME，可从训练好的 gRNA 效率模型中自动反推出"高注意力序列基序"（如 PAM 邻近区、种子区偏好），并与已知生物学知识（如 U6 启动子转录偏好、SpCas9 NGG 需求）交叉验证模型是否学到真实信号而非伪相关。
3. **混淆控制与防泄漏实验设计**：① K562-LenMatch 思路——若正负样本长度/GC 分布不等，模型会利用混淆特征"作弊"，我们构建 gRNA 训练集时必须匹配正负样本的序列长度、GC、PAM 分布；② 染色体级分组交叉验证（整染色体划分）防同源泄漏，直接用于大肠杆菌基因组 gRNA 数据划分（避免同源操纵子/重复区域跨集泄漏）。
4. **TransSHAP 适配 BPE/DNA token 的流程 + 30 次运行取 top-k 稳定性统计**：给出"哪些 k-mer/token 驱动 gRNA 活性预测"的可信清单（频率 + 平均 Shapley 值），可输出为设计规则（如"含 A/T 富集 token 的 gRNA 在高 AT 基因组区域效率更高"）。
5. **打乱扰动实验作为"模型学到了顺序还是组成特征"的诊断**：对 gRNA 序列做碱基打乱/5-bp 块打乱再评估，可判断模型是依赖局部 k-mer 组成还是长程顺序信号——若打乱后性能不降，说明模型没学到顺序特征，需要增加上下文窗口或改架构（M1 模型诊断）。
6. **AT-index 式可解释指标**：把"AT 比例 + motif 频率 + 最长 run + 交替 run"这类可解释复合特征用于大肠杆菌启动子/UTR 区域的 gRNA 位点优先级打分，与黑箱模型输出互为印证（M3 特征层）。

## 6. 与我们方案的冲突/差异点
- 文中酵母 ORI 任务本质上高度依赖强 motif（ACS，>12,000 个匹配中仅 ~500 个功能起点），与我们 gRNA 效率任务的"弱标签 + 多种子多特征"性质不同——其绝对准确率（0.72–0.83）不可直接类比 gRNA 模型性能。
- DNABERT 为人源预训练，直接用于大肠杆菌序列（高 GC、不同调控语法）需验证；且作者明确表示目的不是刷准确率而是可解释性，评测口径（7 折均值）与我们基准任务（如跨物种泛化）不同。
- 其从零训练仅 0.60–0.71 准确率，提示"预训练权重收益主要来自微调"的结论在细菌域未必成立（Evo/细菌专属模型可能更优）——需我们自行消融验证。

## 7. 行动项建议
- **方法论纳入 B2 管线**：实现"注意力→motif 发现（MEME）+ 打乱扰动诊断 + TransSHAP token 归因"三件套，应用于 M1 gRNA 效率模型与 M2 脱靶模型的可解释性分析。
- **数据集规范**：建立 gRNA 正负样本的"特征匹配"检查清单（长度/GC/PAM/启动子类型），并采用染色体级分组交叉验证写入训练流程（防泄漏）。
- 复现其双负样本训练对比实验（随机负 vs 难负），作为 M1 基线改进的实验设计模板。
- 将该文的 ACS/ORI 生物知识（酵母复制起点 ACS 模式）作为"模型学到已知生物信号"的验证基准案例写入 README 的可解释性验证章节。
