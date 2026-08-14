# 文献卡：BioGPT: Generative Pre-trained Transformer for Biomedical Text Generation and Mining

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T4 LLM与Agent |
| 年份 | 2022（Briefings in Bioinformatics 23(6):bbac409；arXiv:2210.10341 发布于 2022-10） |
| 期刊 | Briefings in Bioinformatics（Oxford） |
| DOI | 10.1093/bib/bbac409（arXiv: 2210.10341） |
| 项目映射 | M3（LLM 大模型底座：文献挖掘/问答/关系抽取）、B1（领域知识库与文献知识图谱构建）、D（设计决策支持：从文献抽取基因-酶-代谢物-通路关系） |

## 1. 一句话核心
提出 BioGPT——首个在 1500 万条 PubMed 摘要上从零预训练的生物医学领域生成式 Transformer 语言模型（GPT-2 medium 骨干，347M 参数），通过"把任务标签改写成自然语言目标序列 + source 与 target 之间的软提示（prefix-tuning 连续嵌入）"统一适配下游任务，在 BC5CDR、KD-DTI、DDI 三个端到端关系抽取和 PubMedQA 问答上刷新 SOTA，并展示了优于通用 GPT-2 的生物医学文本生成能力。

## 2. 方法要点（详细）
- **预训练数据**：官方站点抓取 2021 年前所有 PubMed 条目，过滤只有标题无摘要的条目，得 1500 万篇"标题+摘要"作为预训练语料；坚持"领域内数据从零预训练"（引用 PubMedBERT 结论：域内词表与域内数据比在通用模型上继续预训练更优）。
- **词表**：用 fastBPE 在域内语料上学习 BPE 词表（而非沿用 GPT-2 词表），最终词表大小 42,384。
- **模型**：GPT-2 medium 架构（24 层 Transformer decoder、hidden 1024、16 头注意力）；GPT-2 medium 355M 参数，BioGPT 因词表不同为 347M 参数；标准自回归语言建模目标（最小化负对数似然 log P(sⱼ|s₁..sⱼ₋₁)）。
- **预训练配置**：8×NVIDIA V100、200k 步、每 GPU 1024 token、64 步梯度累积（等效 batch 524,288 tokens）；Adam 优化器，峰值学习率 2×10⁻⁴，20,000 步 warm-up，逆平方根衰减。
- **下游任务统一为生成**（关键设计）：
  - 端到端关系抽取：把三元组 ⟨头实体, 尾实体, 关系⟩ 改写为自然语言句子，探索三种格式——svo（"head inhibits tail"）、is-of（"head is the inhibitor of tail"）、rel-is（"the relation between head and tail is inhibitor"）；多三元组按文中出现顺序用分号拼接；实验证明 rel-is 最佳（F1 38.38 > is-of 37.77 > svo 36.57 > 特殊 token 结构化格式 37.32；BC5CDR 上 rel-is 44.98 vs 结构化 42.85，DDI 40.76 vs 38.60）。
  - 问答：source 用 "question: ... context: ..." 前缀拼接，target 为 "the answer to the question given the context is yes/no/maybe"。
  - 文档分类：target 为 "the type of this document is <label>"。
- **Prompt 设计**：采用 prefix-tuning 式软提示（连续嵌入虚拟 token），但插入位置在 source 与 target 之间（[source; prompt; target]）而非序列开头；推理时把 source+prompt 作为前缀让模型续写 target。多数任务用 length=9；KD-DTI 上 length=13 最佳（38.60）；软提示整体优于手工硬提示（"we can conclude that" 38.16 等），且长度在 9–17 间差异不大。
- **微调配置**：单张 V100、1024 token batch、32 步累积；各任务 30–100 epochs（LR 10⁻⁵~10⁻⁴）；关系抽取/QA/分类推理用贪心搜索，文本生成用 beam size=5；评估取最后 5 个 epoch 检查点平均。
- **文本生成评测**：以 KD-DTI 测试集三元组实体（药物/靶点名）为前缀生成描述，无客观指标、以示例展示；另手输 COVID-19 相关关键词验证领域知识（2021 年前语料含 COVID 信息）。
- **规模扩展**：BioGPT-Large 基于 GPT-2 XL（1.5B 参数）。

## 3. 关键结果与指标
- **BC5CDR**（化学-疾病关系抽取，500/500/500 篇）：BioGPT micro-F1 44.98%（P 49.44 / R 41.28），比 REBEL 高 8.28 个百分点、比 seq2rel† 高 4.78 个点（仅用训练集）；用训练+验证集训练达 46.17%；GPT-2 medium 仅 37.39%，GLRE(pred+pred) 仅 8.05%（暴露 NER 误差累积问题）。
- **KD-DTI**（药物-靶点相互作用，12k/1k/1.3k 篇）：F1 38.42%，比 Transformer+PubMedBERT-attn（24.19）高 14.23、比 GPT-2 medium（28.45）高 9.97、比 REBELpt（33.32）高 5.1 个百分点。
- **DDI**（药物-药物相互作用，664/50/191 篇）：F1 40.76%，比 GPT-2 medium（24.68）高 16.08、比 REBEL（28.27）高 12.49、超 REBELpt（40.56）。
- **PubMedQA**：accuracy 78.2%，较此前最佳 BioLinkBERT-large（72.2%）提升 6.0 个百分点，创新纪录（PubMedBERT 55.8%、BioELECTRA 64.2%）。
- **HoC 文档分类**（癌症标志物语料 1,580 篇）：micro-F1 85.12%，超 BioBERT 81.54、PubMedBERT 82.32、BioLinkBERTbase 84.35、GPT-2 medium 81.84。
- **文本生成案例**：对罕见/领域特定词（Apricitabine、CP-673451、BIIB-021 等）GPT-2 生成无关文本甚至数数字，BioGPT 仍能生成专业、流畅的描述；"The drug that can treat COVID-19 is" 前缀下 BioGPT 正确续出 hydroxychloroquine。
- **BioGPT-Large（1.5B）**：BC5CDR 50.12 / KD-DTI 38.39 / DDI 44.89 / PubMedQA 81.0 / HoC 84.40——规模扩大并非所有任务都提升（HoC 略降），说明中等规模 + 域内预训练即可达高性价比。

## 4. 数据与代码可用性
- 代码：https://github.com/microsoft/BioGPT（官方仓库，含模型权重、微调脚本与推理代码）。
- 预训练数据：PubMed 公开抓取（https://ftp.ncbi.nlm.nih.gov/pubmed/）；下游数据 BC5CDR / KD-DTI / DDI 2013 / PubMedQA / HoC 均为公开基准数据集。

## 5. 对我们项目的可借鉴点（重点，结合大肠杆菌氨基酸细胞工厂 + AI-CRISPR 设计）
1. **领域 LLM 的关键配方：域内数据从零预训练 + 域内词表（M3）**：通用 LLM（GPT 系列）在生物医学上表现差是领域偏移所致（作者引用 GPT-3 在生物任务上表现差的研究）；我们若要让 LLM 代理理解大肠杆菌代谢工程文献/CRISPR 文献，应至少在 PubMed/合成生物学语料上继续预训练（或微调），并为项目定制 tokenizer 处理基因名（如 β-alanine、thrA、metL、homoserine 等罕见词）。
2. **"标签→自然语言目标序列"的统一生成范式（M3/B1 可直接复用）**：把结构化任务（关系抽取、分类、QA）改写为自然语言句子，让解码器用同一模块处理输入与输出——我们可用相同思路把"gRNA 序列 → 效率/脱靶标签"改写成 "the predicted cleavage efficiency of guide X is high" 式的文本目标，或让 LLM 直接输出结构化 JSON 式的三元组，便于与预训练分布对齐；其 rel-is 格式（"the relation between A and B is R"）可直接用于构建基因-酶-代谢物-通路知识图谱。
3. **软提示插在 source 与 target 之间 + 连续嵌入（D/M3 工程细节）**：prefix-tuning 提示放在中间优于开头、软提示优于硬提示、长度 9–13 足够——这些可复现的超参经验直接适用于我们用 LLM 做 CRISPR 设计任务（如把"设计约束/底盘信息"作 source、"输出 gRNA 列表"作 target 时插入可学习提示向量）。
4. **端到端关系抽取作为知识库自动构建工具（B1）**：BioGPT 无需中间 NER 标注即可端到端抽取三元组（且优于依赖 NER 的 pipeline，GLRE 用开源 NER 后 F1 从 23.99 崩到 8.05）——我们可用它从合成生物学/代谢工程文献自动抽取"基因-酶-产物-调控关系"，为 AI-CRISPR 设计系统搭建代谢知识图谱，减少人工标注成本。
5. **高质量预训练与微调配置模板**：200k 步、batch 524,288 tokens、峰值 LR 2e-4 + 20k warm-up + 逆平方根衰减、最后 5 epoch 平均、beam=5（生成）——是复现/自训小规模领域 LLM 的现成超参起点。
6. **规模-收益权衡启示**：BioGPT-Large（1.5B）并非全面优于 347M 版本（HoC 反降），说明对我们项目而言优先保证"域内语料质量与任务格式设计"，而不是盲目增大模型；用 300–500M 参数级别模型即可。
7. **领域知识时效性**：BioGPT 因语料截止 2021 而能回答 COVID 相关问题、GPT-2 不能——我们构建 LLM 底座时要注意语料截止时间与 CRISPR 技术（Cas12a 新亚型、碱基编辑）知识的新旧，必要时增量更新语料。

## 6. 与我们方案的冲突/差异点
- 对象是自然语言文献（PubMed 摘要），我们主要处理核苷酸/氨基酸序列与实验数据，需 LLM（文本）与序列模型（DNA/蛋白质）双轨或桥接（如把序列 token 化后以文本格式喂给 LLM），BioGPT 本身不能直接处理序列任务。
- 文本生成评测无客观指标（仅示例），其"流畅"标准不能直接当作我们 gRNA 设计输出质量的评价依据；我们需自行定义客观指标（效率 AUROC、脱靶率等）。
- 关系抽取 F1（38–45%）并不高，说明端到端抽取噪声大——用其构建知识库时必须配人工/规则后验校验，不能全自动入库。

## 7. 行动项建议
- 纳入 M3 基线：评估直接微调 BioGPT（或更新更强的领域模型）做"文献→代谢通路/基因-酶关系抽取"与"CRISPR 设计问答"两个 demo，对比通用 LLM。
- 复现其标签改写与提示工程：在 LLM 代理的 gRNA 输出模块采用 [source; 软提示; target] 结构与 rel-is 式自然语言目标，写入 README 工程规范。
- B1 知识库：用其端到端三元组抽取流程 + 人工审核，从大肠杆菌代谢工程文献构建"基因-酶-产物-调控"知识图谱，作为 AI-CRISPR 靶点推荐的先验知识源。
- 记录超参模板：域内 BPE 词表（42k 级）、batch 524k tokens、逆平方根 LR 调度等，作为自训/微调领域 LLM 的默认配置写入实验文档。
