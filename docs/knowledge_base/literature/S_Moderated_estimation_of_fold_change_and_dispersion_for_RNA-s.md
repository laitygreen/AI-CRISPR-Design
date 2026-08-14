---
# 文献卡：Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T6 生信管线（转录组差异分析统计方法） |
| 年份 | 2014 |
| 期刊 | Genome Biology, 15:550 |
| DOI | 10.1186/s13059-014-0550-8 |
| 项目映射 | B2（多组学差异分析管线核心组件）；B3（数据质控/归一化）；间接支撑 M3（gRNA 靶点/编辑效果验证）与 T5（细胞工厂表型组学分析） |

## 1. 一句话核心
DESeq2 提出基于负二项 GLM 的经验贝叶斯收缩（shrinkage）估计框架：对离散度（dispersion）按均值趋势收缩、对 log2 倍数变化（LFC）按零中心先验收缩，显著提升低重复数 RNA-seq 差异分析中效应量与离散度估计的稳定性、可解释性与跨批次可复现性，并内置阈值检验、离群点检测与 rlog 方差稳定变换。

## 2. 方法要点（详细）
- **模型**：Kij ~ NB(mean μij, dispersion αi)，μij = sij·qij，log qij = Σr xjr·βir；默认 size factor sj 用 median-of-ratios 估计（几何平均参照）；支持基因特异归一化因子（cqn、EDASeq）与复杂设计矩阵；多水平因子用 expanded design matrix（避免基水平不收缩）。
- **离散度收缩（三步近似经验贝叶斯）**：① 单基因 MLE 估计 αgw（Cox–Reid 调整似然，校正拟合值估计偏差，Fisher 信息 det(XᵀWX)）；② 用 gamma 族 GLM 拟合离散度-均值趋势 αtr(μ̄)=a1/μ̄+α0（迭代剔除 ratio 超出 [1e-4, 15] 的离群点，直到系数平方和变化 <1e-6）；③ log-normal 先验 + MAP 最终估计；先验宽度 σd² = max(s²lr − ψ1((m−p)/2), 0.25)（MAD 稳健估计；残差自由度 ≤3 时用模拟+KL 散度估计）；离散度离群点（残差 > 2·slr 高于趋势线）不收缩、直接用基因特异估计。
- **LFC 收缩**：对非截距系数设零中心正态先验 N(0, σr²)；σr 由 MLE LFC 的经验分布分位数匹配（p=0.05，剔除 |LFC|>10 的极端值，因子多水平时对全部对比取平均）获得；MAP 估计通过带 ridge 惩罚 λr=1/σr² 的 IRLS（iteratively reweighted ridge regression）求解；收缩强度取决于观测 Fisher 信息（低计数/高离散/少自由度 → 强收缩）。
- **检验**：Wald 检验（收缩 LFC / 后验 SE）；BH 校正 FDR；自动独立过滤（以平均归一化计数为过滤统计量，自动选择在目标 FDR 下最大化检出基因数的阈值，基于 Basu 定理保证不破坏 I 类错误控制）；可选复合零假设检验 |βir|≤θ（找显著超阈值的基因）和 |βir|≥θ（找显著弱效应的基因，需关闭 LFC 收缩）。
- **离群点处理**：Cook's distance > F(p, m−p) 的 0.99 分位数判定离群；条件重复数 ≤6 → 整基因剔除（含多重检验校正）；≥7 → 用 trimmed mean（按 size factor 缩放）替换离群计数后重估。
- **rlog 变换**：以"每样本指示变量 + 截距"设计矩阵做无监督收缩拟合（blind dispersion），得到近似同方差的 log2 尺度值，用于 PCA/聚类/热图；处理了大 size factor 动态范围（≥4）时 VST 的伪影；大计数时 rlog ≈ log2(Kij/sj)。
- **基准测试**：① 模拟：10,000 基因 NB 计数（均值/离散度取自 Pickrell 数据联合分布），样本数 m∈{6,8,10,20}，80% 零假设、20% 真实 FC∈{2,3,4}，以 adjusted P<0.1 计算敏感性/精度；② 真实数据：Pickrell（淋巴母细胞系，26 个 46bp 样本随机 5v5 分 30 次估 FPR）、Bottomly（两品系小鼠纹状体，10v11，3v3 评估/7v8 验证分 30 次估敏感性，逐算法轮转确定验证集 calls）；对比 DESeq(旧)、edgeR（±robust）、DSS、EBSeq、voom+limma、SAMseq、Cuffdiff 2；③ LFC 精度对比 GFOLD、edgeR predictive LFC；④ 聚类对比 rlog/VST/Poisson 距离。

## 3. 关键结果与指标
- 模拟：DESeq2 与 edgeR 在控制实际 FDR≤0.1 的算法中常具有最高敏感性，尤其对小效应量（FC=2 或 3）优势明显；旧 DESeq 过度保守。
- LFC 可复现性：Bottomly 数据对半拆分，按 MLE LFC 排序的 top-100 基因两组重叠仅 21/100，按收缩后 MAP LFC 排序重叠升至 81/100（RMSE 显著下降）。
- FPR：全部算法基本控制 I 类错误（nominal 0.01）；旧 DESeq 与 Cuffdiff 2 偏保守。
- 敏感性（3v3 评估集）：各算法中位敏感性 0.2–0.4；DESeq2 与 edgeR、voom 相当、低于 DSS；校准到中位实际精度 0.9 后 DESeq2 常位居中位敏感性前列。
- 精度：DESeq2 常居第二高中位精度（仅次于旧 DESeq）。
- 离群点模拟：DESeq2 与 edgeR-robust 在含离群点数据上几乎恢复无离群点性能。
- rlog 在 size factor 不相等时聚类恢复（调整 Rand index）优于其他变换。
- 方法适用范围：ChIP-seq、barcode 实验、宏基因组计数、核糖体谱、CRISPR/Cas 文库筛选（文中引用 ref 46 的 CRISPR 文库应用）等各类 HTS 计数数据。

## 4. 数据与代码可用性
- R/Bioconductor 包：http://www.bioconductor.org/packages/release/bioc/html/DESeq2.html（带完整 vignette）。
- 可复现代码包 DESeq2paper（Sweave vignettes，重现全部图表）：http://www-huber.embl.de/DESeq2paper。
- 数据：Pickrell SRA:SRP001540（GRCh37/Ensembl 70）、Bottomly SRA:SRP004777（NCBIM37/Ensembl 66）、Hammer（ReCount 资源）；TopHat2 比对 + summarizeOverlaps/htseq-count/featureCounts 计数。
- 许可：CC BY 4.0（BioMed Central Open Access）。

## 5. 对我们项目的可借鉴点（重点，结合大肠杆菌氨基酸细胞工厂 + AI-CRISPR 设计）
1. **经验贝叶斯收缩直接移植到我们的多组学管线（B2）**：β-丙氨酸/L-高丝氨酸菌株改造的转录组对比往往只有 3–4 个生物学重复，DESeq2 的离散度-均值趋势收缩 + LFC 收缩是标准解法；建议把 DESeq2 设为"改造前 vs 改造后 / gRNA 敲除 vs 对照"差异分析的默认工具，并报告 shrunken LFC 而非原始 MLE LFC。
2. **效应量阈值检验（|β|≤θ）适合筛选"生物学显著"的改造相关基因**：传统零假设检验在大样本下会把微小但显著的表达变化列入清单；用阈值检验直接筛选 |log2FC|≥1 的基因，输出更适合代谢工程师决策的候选列表（T5 通路基因优先级排序）。
3. **独立过滤 + FDR 流程提升低表达基因检出**：我们的 gRNA 靶基因（如通路酶基因）常有中低表达，独立过滤（按均值计数过滤后再做多重检验校正）可显著提升小样本差异分析功效——写入管线默认参数。
4. **Cook's distance 离群点策略可复用于 CRISPR 筛选数据**：文中明确 DESeq2 可用于 CRISPR/Cas 文库筛选计数；我们做 gRNA 文库（如 dCas9 抑制文库）筛选中，可用同样的离群点替换/剔除规则处理污染孔或批次异常样本。
5. **rlog/方差稳定变换作为机器学习输入预处理**：用 rlog 变换后的表达矩阵（同方差）喂给我们的聚类/回归/LLM 分析模块（如菌株代谢表型-基因表达关联建模），避免异方差使低表达基因主导距离计算（B3 特征工程）。

## 6. 与我们方案的冲突/差异点
- DESeq2 的 LFC 收缩默认"向零收缩"，对希望凸显大幅改造效果（如 β-丙氨酸通路酶基因过表达几十倍）的场景会低估效应量——报告时应同时给出 MLE 与 shrunken LFC，或在展示时明确说明收缩意图。
- 对重复数为 2 的条件无法做 Cook's 离群点检测；我们实验设计应尽量 ≥3 重复。
- 基因级计数会掩盖同工酶/异构体层面的变化（对细菌影响小，但要注意多顺反子转录单位——大肠杆菌操纵子计数需按 TU 聚合）。

## 7. 行动项建议
- 将 DESeq2（含阈值检验、独立过滤、rlog）固化为 B2 转录组差异分析子管线的默认组件，写入 README 与管线代码。
- 制定"≥3 生物学重复"实验设计规范，并建立 shrunken LFC + FDR<5% + |log2FC|≥1 的报告模板（T5 表型-表达关联分析）。
- 用 DESeq2 处理 CRISPR 文库筛选计数（Bar-seq/筛选计数），评估 gRNA 靶基因对菌株适应度的影响（M1/M2 验证环节）。
