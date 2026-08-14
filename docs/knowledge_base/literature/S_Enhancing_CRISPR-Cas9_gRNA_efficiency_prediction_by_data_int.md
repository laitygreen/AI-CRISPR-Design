# 文献卡：Enhancing CRISPR-Cas9 gRNA efficiency prediction by data integration and deep learning

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T1 gRNA效率 |
| 年份 | 2021 |
| 期刊 | Nature Communications |
| DOI | 10.1038/s41467-021-23576-0 |
| 项目映射 | M1（gRNA效率预测） |

> 注：M1–M4/B1–B3/D 模块编号按项目背景（gRNA效率预测、脱靶评估、细胞工厂设计、LLM/Agent、基础支撑）推断映射。

## 1. 一句话核心
用慢病毒替代载体（surrogate vector）高通量测定 10,592 条 SpCas9 gRNA 在细胞内的编辑活性，再与 Kim et al. (2019) 数据按重叠序列线性 rescale 融合成 23,902 条 gRNA 数据集，训练"序列 CNN + 热力学结合能 ΔGB"的深度学习模型 CRISPRon，在 4 个与训练数据无重叠的外部独立测试集上显著优于 Azimuth、DeepSpCas9、DeepHF、DeepSpCas9variants。

## 2. 方法要点（详细）
- **实验数据生成**：12,000 条 gRNA oligo（每条 170 bp：BsmBI 位点+U6 转录起始"g"+20 bp spacer+82 bp scaffold+37 bp surrogate target（10 bp 上游+20 bp protospacer+3 bp PAM+4 bp 下游）+linker），靶向 DGI db 药物靶点库中约 7000 基因（最终 3834 个基因、3832 个靶基因，覆盖每个基因前 3 个编码外显子，用 FlashFry v1.80 剔除 hg19 中 0–3 bp 错配潜在脱靶并排序）；Golden Gate（BsmBI）组装质粒库→PEI 转染 HEK293T 包装慢病毒（MOI=0.3、每 gRNA 覆盖约 4000 细胞）→转导 HEK293T-SpCas9；Day2/8/10 靶向扩增子测序（MGISEQ-2000，PE150，深度>1000；fastp 过滤、FLASH 合并、BWA-MEM 比对）；总编辑效率=（非 37 bp 读段数/总读段数）%；Day8 与 Day10 活性 Spearman R=0.91，取平均→10,592 条高质量 gRNA（10,313 条为本研究独有；Dox 过表达组剔除）。
- **数据验证与整合**：surrogate 位点与 16 个对应内源位点 indel 频率 Spearman R=0.72（p=0.0016）；与 Kim 2019、Wang 2019 共同 gRNA 的 Spearman R=0.67（两者间仅 0.52）；与 Kim 2019 用 49 对重叠 30mer 拟合线性回归做 rescale 融合→23,902 条 30mer；预处理过滤规则：不在 hg38、无 GENCODE v32 注释、实验间高方差（上四分位+1.5×IQR）、目标基因 <10 条 gRNA、非 NGG PAM、tRNA 系统、靶向 CDS 最后 10%；loss-of-function 类数据（Xu/Hart/Doench）与 indel 类数据（Kim/Wang/Chari）分类处理，非 indel 数据用 SciPy rankdata 归一化。
- **特征**：30mer 输入＝20 nt protospacer＋4 nt 上游＋3 nt PAM＋3 nt 下游；one-hot 位置特异单/双核苷酸；NGG 两侧碱基二值化（NGGX_YZ）；1/2 nt 滑窗计数；GC 含量；Biopython 1.77 Tm_staluc 计算 protospacer 三段（3–7、8–15、16–20）熔解温度；RNAfold 2.2.5 + CRISPRoff 1.1.1 能量模型计算 spacer 折叠自由能与 ΔGB（gRNA-DNA 杂交自由能＋DNA-DNA 解链＋RNA 解开惩罚）。
- **模型**：one-hot 30mer → 3/5/7 三种尺寸卷积核 → 展平 → 全连接；卷积输出先收集到一个全连接层再与 ΔGB 拼接（此设计 MSE 144.73→140.83，优于三 FC 直拼与直接拼接 143.15→141.76）；Keras/TensorFlow 2.2.0、Python 3.8.3；ADAM、lr=0.0001（对 0.001/0.0005/0.0001/0.00005 网格筛选）、batch=500、验证集 100 epoch 无提升即早停（总 500–1500 epoch）；6 分区 6-fold CV，每折 10 次随机重复取最优，最终输出 6 个最优模型预测平均。
- **数据划分与去泄漏**：按 one-hot 30mer 两两 Hamming 距离聚类，Hamming ≤8（≤4 nt 差异）的相似 gRNA 归入同一 partition，共 6 个等大分区；测试集再剔除与任何对比模型训练集 ≤3 nt 差异（Hamming ≤6，20 nt spacer 空间）的 gRNA。
- **特征重要性**：GBRT（lr∈[0.08,0.1]、深度∈[3,5,7]、树数∈[400,1000] 等网格）+ SHAP + Gini importance。

## 3. 关键结果与指标
- 内部独立测试集：CRISPRon Spearman R=0.80，超过 Azimuth 0.56、DeepSpCas9 0.73、DeepHF 0.74（DeepSpCas9variants 的 N.a. 表示其训练集含全部 gRNA）。
- 外部独立测试集（>1000 gRNA）：CRISPRon R≈[0.46,0.68]，对比 Azimuth [0.36,0.45]、DeepSpCas9variants [0.25,0.31]、DeepSpCas9 [0.44,0.52]、DeepHF [0.42,0.46]。
- 特征分析（SHAP 与 Gini 一致）：ΔGB 是最主要贡献特征；其次是 GC 含量、spacer 折叠自由能；PAM 近端两个碱基 G/A 优于 C/T；TT 双核苷酸（弱结合自由能）不利。
- 数据兼容性：pre-CRISPRon_v0 与 DeepSpCas9 互测 Spearman R>0.70，证明两个独立高通量数据集高度兼容、可融合。

## 4. 数据与代码可用性
- 测序数据：GEO GSE173708、中国国家基因库 CNP0001031；gRNA 效率数据见 Supplementary Data 1；替代载体 Addgene #170459；代码 https://github.com/RTH-tools/crispron（Zenodo 10.5281/zenodo.4725572）；交互式设计服务 https://rth.dk/resources/crispr/（集成 IGV）。

## 5. 对我们项目的可借鉴点
1. **替代载体高通量活性测定思路**：surrogate vector 活性与内源位点高度相关（R=0.72）；我们可在 E. coli 中构建靶向 β-丙氨酸/L-高丝氨酸代谢通路基因的 sgRNA 质粒文库批量测活性，以最低湿实验成本扩充 M1 训练标注。
2. **跨数据集线性 rescale 融合协议**：用重叠序列（49 对）拟合线性回归统一不同文献的效率尺度，并先验证数据集间 Spearman>0.7 再融合——我们整合多个 E. coli sgRNA 数据集时必须照做并报告兼容性。
3. **ΔGB 热力学特征显式入模**：加入 gRNA-DNA 结合自由能显著降 MSE（144.73→140.83），且 SHAP 证明其第一重要；对 E. coli 用 ViennaRNA/RNAfold 即可复现，成本极低、收益明确。
4. **严格相似性分区与去泄漏**：30mer Hamming≤8 聚类分区、测试集剔除 ≤3 nt 相似 gRNA——这是防止"性能虚高"的关键协议，直接写入我们 M1/B2 评估规范。
5. **训练协议**：早停（100 epoch）+ 6 折×10 次重复取平均 + lr 网格筛选，作为我们模型训练的默认配置。
6. **交付形态**：交互式 webserver + IGV 可视化提示我们把 gRNA 设计/评分结果做成可交互界面（B3/展示模块）。

## 6. 与我们方案的冲突/差异点
- 数据与模型均为人类细胞系 SpCas9 NGG；E. coli 基因组 GC≈50.8%、无染色质域、操纵子结构不同，上下文窗口（4 nt 上游+3 nt 下游）与权重不能直接迁移，需用 E. coli 数据重训并重新验证窗口设计。
- surrogate 方法不捕获大片段缺失/染色体重排等编辑结局；若我们评估的是基因敲除（knockout）成功率需注意活性口径差异。
- 其融合数据含大量人源基因上下文，对原核启动子/终止子区域（如我们改造代谢基因操纵子）无覆盖。

## 7. 行动项建议
- 下载 23,902 条 gRNA 数据与 CRISPRon 代码，作为 M1 外部验证集与复现基线（按 ≤3 nt 相似性剔除重叠）。
- 将"ΔGB+GC+折叠自由能"特征池与"相似性分区/早停/多折平均"训练协议纳入 M1 模型开发规范。
- 在 README 记录其数据融合与去泄漏协议，作为我们多组学数据整合的参考标准。
