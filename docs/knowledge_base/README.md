# AI-CRISPR 智能设计系统 · RAW 知识库（分模块设计）

> 版本 v1.1 | 日期 2026-08-14 | 用途：备赛知识沉淀 + 生信方法指导 + 大模型训练建议
> 结构：每个模块 = 项目流程步骤 × 文献支撑 × 生信方法指导 × 大模型训练建议

---

## 一、知识库文件清单

| 文件 | 内容 |
|---|---|
| 00_数据工程与生信层.md | 模块 M0（数据工程）+ B1（位点扫描）+ B2（多组学）+ B3（表型关联） |
| 01_gRNA效率与脱靶模块.md | 模块 M1（gRNA 效率预测）+ M2（脱靶评估） |
| 02_大模型与验证闭环.md | 模块 M3（基因型-表型大模型）+ M4（设计 Agent）+ D（湿实验闭环） |
| 03_项目流程总览.md | 全流程步骤表 + 里程碑 + 风险应对 |
| literature/ | 25 篇已下载文献的精读文献卡（每篇含方法/指标/借鉴点/行动项） |

## 二、模块总览

| 模块 | 名称 | 项目流程环节 | 核心文献 | 生信方法 | 大模型训练 |
|---|---|---|---|---|---|
| M0 | 数据工程 | 数据采集/标准化 | Doench/DeepCRISPR 数据集 | pandas 清洗、DVC 版本 | 数据增强/去偏 |
| M1 | gRNA 效率预测 | 靶点设计后效率评分 | DeepCRISPR/CRISPRon/DNABERT-2 | 序列特征工程 | DNA 预训练+微调 |
| M2 | 脱靶风险评估 | 特异性筛选 | GUIDE-seq/CIRCLE-seq/CRISPR-Net | 比对+特征融合 | CNN/Transformer 分类 |
| M3 | 基因型-表型大模型 | 靶点推荐/机制解析 | LLM 代谢工程设计/BioGPT/BioT5 | 多组学关联分析 | LLM LoRA+RAG |
| M4 | 靶点设计 Agent | 端到端工作流 | CRISPR-GPT | 规则引擎+API 编排 | Prompt 工程+评测 |
| B1 | CRISPR 位点扫描 | 全基因组候选枚举 | CRISPOR 方法学 | PAM 搜索/保守性 | 序列 embedding 排序 |
| B2 | 多组学机制解析 | 瓶颈识别 | iML1515/DESeq2/breseq | FBA/WGS/RNA-seq | 通量特征+因果推断 |
| B3 | 基因型-表型关联 | 靶点优先级 | 细胞工厂文献 | SHAP/统计关联 | 多模态融合 |
| D | 湿实验验证闭环 | AI设计→实验→回流 | 课题 1/2/3 方法 | 编辑/发酵/测序 | 主动学习迭代 |

## 三、文献卡目录（25 篇）

| 文献 | 分级 | 主题 | 卡文件 |
|---|---|---|---|
| DeepCRISPR (2018) | S | T1 gRNA效率 | S_DeepCRISPR_optimized_CRISPR_guide_RNA_design_by_deep_learnin.md |
| CRISPRon/CRISPRoff (2021) | S | T1 gRNA效率 | S_Enhancing_CRISPR-Cas9_gRNA_efficiency_prediction_by_data_int.md |
| Improved off-target with DNABERT (2025) | S | T2 脱靶 | S_Improved_CRISPR_Cas9_Off-target_Prediction_with_DNABERT_and_.md |
| ML+DL on/off-target review (2023) | A | T1/T2 | A_Using_traditional_machine_learning_and_deep_learning_methods.md |
| DL in CRISPR review (2023) | A | T1/T2 | A_Deep_learning_in_CRISPR-Cas_systems_a_review_of_recent_studi.md |
| CRISPR computational survey (2022) | A | T1/T2 | A_CRISPR_genome_editing_using_computational_approaches_A_surve.md |
| DNA foundation benchmark (2025) | A | T3 DNA底座 | A_Benchmarking_DNA_foundation_models_for_genomic_and_genetic_t.md |
| DVPNet XAI (2026) | A | T3 DNA底座 | A_DVPNet_A_New_XAI-Based_Interpretable_Genetic_Profiling_Frame.md |
| Genos GFM (2025) | A | T3 DNA底座 | A_Genos_a_human-centric_genomic_foundation_model_.md |
| DNA replication origins DNABERT (2026) | A | T3 DNA底座 | A_Interpretable_prediction_of_DNA_replication_origins_in_S_cer.md |
| Listeria DNABERT+SHAP (2026) | A | T3 DNA底座 | A_Listeria_Genome_Identification_Using_DNABERT_Embedding_With_.md |
| BioGPT (2022) | S | T4 LLM | S_BioGPT_generative_pre-trained_transformer_for_biomedical_tex.md |
| LLM for Metabolic Engineering (2024) | S | T4 LLM | S_Leveraging_Large_Language_Models_for_Metabolic_Engineering_D.md |
| CRISPR-Cas12a via LLM (2024) | S | T4 LLM | S_Novel_CRISPR-Cas12a_Clades_Discovery_Using_Large_Language_Mo.md |
| Generanno GFM (2025) | A | T3/T4 | A_Gener_i_anno_i_A_Genomic_Foundation_Model_for_Metagenomic_An.md |
| DCVBin (2026) | A | T3 应用 | A_DCVBin_a_novel_binning_method_for_single-sample_metagenomes_.md |
| Delivering CRISPR review (2018) | A | 递送（背景） | A_Delivering_CRISPR_a_review_of_the_challenges_and_approaches_.md |
| L-Homoserine strategies (2024) | S | T5 课题3 | S_Metabolic_engineering_strategies_for_L-Homoserine_production.md |
| POP 氨基酸综述 (2024) | S | T5 课题1/3 | S_Recent_Advances_in_Metabolic_Engineering_for_the_Biosynthesi.md |
| L-alanine production (2022) | A | T5 类比 | A_L-alanine_production.md |
| E. coli arginine (2015) | A | T5 类比 | A_Metabolic_engineering_of_Escherichia_coli_for_enhanced_argin.md |
| Evolved E. coli omics (2010) | A | T6 多组学 | A_Omic_data_from_evolved_E_coli_are_consistent_with_computed_o.md |
| DESeq2 (2014) | S | T6 生信 | S_Moderated_estimation_of_fold_change_and_dispersion_for_RNA-s.md |
| RegulonDB v10.5 (2019) | S | T6 数据库 | S_RegulonDB_v10_5_tackling_challenges_to_unify_classic_and_hig.md |
| EcoCyc (2013, DOI已修正) | S | T6 数据库 | S_EcoCyc_a_comprehensive_database_of_E_coli_biology.md |

## 四、质量与注意事项

- 25 篇文献卡由 5 个并行精读代理生成，均基于全文精读（非摘要）
- ⚠️ EcoCyc 条目曾发生 PDF 内容错配（Unpaywall 映射错误），已修正元数据与文献卡；正确 PDF 需从 PMC3531154 手动获取，详见 literature/00_注意_文件内容错配警告.md
- 建议对关键 S 级 PDF 抽查文件头与标题一致性

## 五、目录规划

knowledge_base/
├── README.md                  # 本索引
├── 00_数据工程与生信层.md      # M0+B1+B2+B3
├── 01_gRNA效率与脱靶模块.md    # M1+M2
├── 02_大模型与验证闭环.md      # M3+M4+D
├── 03_项目流程总览.md          # 全流程
└── literature/                # 25 篇文献卡 + 引文库

