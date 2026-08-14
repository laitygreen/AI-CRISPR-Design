# 文献卡：Using traditional machine learning and deep learning methods for on- and off-target prediction in CRISPR/Cas9: a review

| 字段 | 内容 |
|---|---|
| 分级 | A |
| 主题 | T1 gRNA效率 + T2 脱靶（综述，覆盖两类任务） |
| 年份 | 2023 |
| 期刊 | Briefings in Bioinformatics |
| DOI | 10.1093/bib/bbad131 |
| 项目映射 | M1、M2、B2（基线与评估支撑模块） |

> 注：M1–M4/B1–B3/D 模块编号按项目背景（gRNA效率预测、脱靶评估、细胞工厂设计、LLM/Agent、基础支撑）推断映射。

## 1. 一句话核心
系统综述并横向对比了 CRISPR/Cas9 on-target（gRNA 效率）与 off-target（特异性）预测中传统机器学习（SVM/RF/GBRT/XGBoost 等）与深度学习（FNN/CNN/RNN/LSTM/注意力）两大类方法，梳理了基准数据集、序列编码方案（one-hot 与 word embedding）与关键结论（大样本下 DNN 更优、数据不平衡与特征工程是核心瓶颈、简单模型在小数据上可反超 DL），并开源了整理后的数据集与预处理脚本。

## 2. 方法要点（详细）
- **数据集盘点（三类）**：
  - 仅 off-target：GUIDE-seq（Tsai 2015，28 个 OTS，VEGFA/HEK293 等位点）；CIRCLE-seq（10 条 gRNA，7371 个活性 OTS，含 bulge）；SITE-seq（9 条 gRNA，3767 个活性 OTS）；Abadi et al. 2017（GUIDE-seq+HTGTS+BLESS，33 组 sgRNA、872 个基因组靶点）；CHANGE-seq（110 条 sgRNA、13 个人原代 T 细胞位点、201,934 个 OTS，单 sgRNA OTS 数 19–61,415）。
  - 仅 on-target：Wang 2014（73,000 sgRNA）；Koike-Yusa 2014（87,897 gRNA/19,150 小鼠基因）；Doench V1（1831 guides，3 人+6 鼠基因）；GenomeCRISPR（>55 万 sgRNA/84 实验）；DeepHF（>50,000 gRNA/核酸酶、约 20,000 基因，哺乳动物最大）；DeepSpCas9（12,832 靶点）；sgDesigner（12,472 oligo）。
  - 两者兼有：Doench V2（2549 guides/8 基因/A375 细胞）；CRISPOR 数据库（聚合 Wang-Xu、Koike-Yusa、Hart、Chari、Z_fish 等 22 个数据集，支持 >150 基因组）；DeepCRISPR（约 6.8 亿 sgRNA/13 细胞系，含表观特征）。
- **序列编码**：one-hot 家族（4×23 朴素矩阵；Lin 4×23；Charlier 无信息损失的 8×23 双射编码；Lin 7×23＝5-bit 字符通道(A,C,G,T,_)＋2-bit 方向通道，显式编码 mismatch/插入/缺失；Zhang 20×L 含 12-bit 错配通道）；word embedding（Word2Vec；GloVe＋BiLSTM＋CNN 的 CnnCrispr；Keras Tokenizer 的 label-encoding）。
- **传统 ML 代表工作与指标**（表 2）：Wang 2014 SVM（log2 fold change）；Doench 2014 logistic 回归 AUROC 0.8；Xu 2015 Elastic-Net AUROC 0.73；Fusi 2015 GBRT Spearman 0.52/AUROC 0.75；Doench V2 2016 对比 8 种 ML（off-target AUROC 0.8、on-target Spearman 0.54）；Rahman CRISPRpred（SVM）AUROC 0.85/AUPRC 0.56/MCC 0.4；Abadi CRISTA（RF 回归）Spearman 0.81/AUROC 0.96/AUPRC 0.96/R²=0.8；Peng 2018 集成 SVM AUROC 0.99/AUPRC 0.45；Schoonenberg CRISPRO Spearman 0.57；Listgarten Elevation AUROC 0.98；Chen CRISPEY（23,936 样本）SVM 召回 64%、logistic 准确率 94%；Zhang 2019 AdaBoost 集成 AUROC 0.938/AUPRC 0.299；Lazzarotto CHANGE-seq（GTB）AUROC 0.995/AUPRC 0.881；Rafid CRISPRpred(SEQ)（SVM＋位置特征＋n-gapped dinucleotide）Spearman 0.829/AUROC 0.893，4 个细胞系中 3 个超过 DeepCRISPR；He GuidePro（两层集成）Spearman 0.523；Wang GNL-Scorer Spearman 0.502（跨物种）；Dhanjal AUROC 0.97/准确率 91.49%；Hiranniramol sgDesigner（SVM+XGBoost 堆叠）Spearman 0.75/AUROC 0.934/准确率 86.3%；Konstantakos CRISPRedict Spearman 0.380(U6)/0.355(T7)、nDCG 0.805；Zarate BoostMEC（LightGBM＋贝叶斯超参）Spearman 0.78，在 13 个基准集上优于多数 DL。
- **深度学习代表工作与指标**（表 4）：DeepCRISPR（Spearman 0.246/AUROC 0.804/AUPRC 0.303）；Lin 2018 CNN AUROC 97.2%；Xue DeepCas9（1D-CNN）Spearman 0.23–0.61；Liu seqCrispr Spearman 0.77；Wang DeepHF（RNN）Spearman 0.867/0.862/0.860；Shrawgi DeepSgRNA Spearman 0.82/AUROC 0.85；Liu AttnToMismatch_CNN（Transformer+2D-CNN）AUROC 0.961、AttnToCrispr_CNN Spearman 0.778/Pearson 0.781；Kim DeepSpCas9（3×1D-CNN）Spearman 0.73；Liu CnnCrispr（GloVe+BLSTM+CNN）AUROC 0.957/AUPRC 0.429；Zhang DL-CRISPR（图像式增强）准确率 98.57%/灵敏度 95.13%；Zhang CNN-SVR AUROC 0.94/Spearman 0.7；Chen DNA-BERT＋LightGBM AUROC 0.993/AUPRC 0.594/Spearman 0.276；Zhang C-RNNCrispr AUROC 0.976/Spearman 0.877；Trivedi Crispr2vec AUROC 0.91（未见 sgRNA）；Lin CRISPR-Net（LRCN）AUROC 0.995/AUPRC 0.317；Zhang CRISPR-OFFT AUROC 0.97/AUPRC 0.79、CRISPR-ONT AUROC 0.865；Xiao AttCRISPR Spearman 0.872；Charlier（8×23 编码）AUROC 0.995/AUC-PR 0.949/准确率 99.9%；Störtz piCRISPR（物理特征）AUROC 0.983/AUPRC 0.978；Xiang CRISPRon/CRISPRoff Spearman 0.91；Niu R-CRISPR AUROC 0.991/AUPRC 0.319；Vinodkumar GCN-CRISPR AUROC 0.987；Zhang CRISPR-IP（CNN+BLSTM+attention）AUROC 0.982/AUPRC 0.751/准确率 0.990；Elkayam DeepCRISTL（BLSTM+迁移学习）Spearman 0.878；Fu MOFF（双 CNN 回归）Spearman 0.5。
- **不平衡处理**：数据增强（DL-CRISPR 把 sgRNA-DNA 编码矩阵旋转 90/180/270 度把正样本×4；CNN 四层）；负类下采样（CnnCrispr）。
- **未来方向**：迁移学习（Lin/Charlier 已用 CRISPOR→GUIDE-seq）、超参数优化（贝叶斯/网格/进化）、可解释性（SHAP/Tree SHAP/Deep SHAP）、不确定性量化（aleatoric/epistemic）、主动学习。

## 3. 关键结果与指标
- 综述核心结论：①序列编码（尤其含 indel/mismatch 显式通道的 7×23/8×23 无信息损失编码）显著影响性能；②集成方法（AdaBoost/RF/GBRT）普遍优于单一非集成方法；③特征工程（熔解温度、分子量、microhomology、ΔGB 等）是提升关键；④off-target 数据极端不平衡，须增强或重采样；⑤数据量足够大时 DNN 优于评分方法与传统 ML，但小数据下简单模型（BoostMEC Spearman 0.78、CRISPRpred(SEQ) 等）可反超 DL；⑥注意力机制提升性能与可解释性；⑦多数公开数据集正负样本数不可比，类别不平衡负面影响两类方法。
- 代表性数值（供基线对照）：DeepHF Spearman 0.867、DeepSpCas9 0.73、CRISPRon 0.91、CRISPR-IP AUROC 0.982、piCRISPR AUROC 0.983、CHANGE-seq GTB AUROC 0.995 等。

## 4. 数据与代码可用性
- 整理后的基准数据集与 one-hot 预处理脚本：https://github.com/dagrate/public_data_crisprCas9；各原始数据集链接见表 1（GUIDE-seq/CIRCLE-seq/SITE-seq/CHANGE-seq/DeepHF/DeepSpCas9/CRISPOR/GenomeCRISPR/Doench V1/V2 等）。

## 5. 对我们项目的可借鉴点
1. **数据集与基线"路线图"**：表 1/2/4 是 M1/M2 数据集选型与复现基线清单的现成素材，可直接挑选可迁移数据（DeepHF、DeepSpCas9、CRISPRon、sgDesigner 等）并登记入训练集清单。
2. **编码方案对比结论**：支持 indel/bulge 的 7×23/8×23 编码优于朴素 4×23——我们的 E. coli off-target 模型输入应显式编码 mismatch/插入/缺失，避免信息损失。
3. **"简单基线优先"**：BoostMEC、CRISPRpred(SEQ) 在小数据/特征工程充分时反超 DL；我们 M1/M2 对比矩阵必须包含 LightGBM/XGBoost/SVM 基线，防止"模型复杂度虚高"。
4. **不平衡工具箱**：旋转式数据增强（DL-CRISPR）、负类下采样、mini-batch 平衡采样三种方案直接移植到脱靶训练。
5. **可解释性方法栈**：SHAP/Tree SHAP/Deep SHAP 特征归因与我们的 LLM 解释模块联动，输出"哪些位置/特征驱动预测"。
6. **主动学习与不确定性量化**：低置信度 gRNA 优先送湿实验验证，形成"预测→验证→回灌"闭环（E. coli 标注成本高时尤其划算）。

## 6. 与我们方案的冲突/差异点
- 综述覆盖以人源/真核为主，大肠杆菌（原核、小基因组 ~4.6 Mb、无染色质域）内容少；文中 Wang & Zhang 2019 细菌 E. coli CNN（Spearman 0.582/0.7105/0.360）表明物种特异模型必要——支持我们自建 E. coli 模型而非直接移植人源工具。
- 各工具指标来自不同数据集与划分，不能直接横向比较；引用综述数值前须在统一去泄漏协议下重测（这正是我们 B2 评估模块的职责）。

## 7. 行动项建议
- 从 https://github.com/dagrate/public_data_crisprCas9 下载整理数据集，纳入训练集与外部验证集清单。
- 建立"简单基线优先、统一去泄漏协议"的评测流程：先 LightGBM/SVM/XGBoost，再 DL，逐项登记指标。
- 将"支持 indel 通道的编码、不平衡处理、SHAP 归因"三部分写入 README 技术选型章节。
