---
# 文献卡：Metabolic engineering of microorganisms for L-alanine production（微生物代谢工程生产L-丙氨酸）

| 字段 | 内容 |
|---|---|
| 分级 | A |
| 主题 | T5 细胞工厂 |
| 年份 | 2022 |
| 期刊 | Journal of Industrial Microbiology and Biotechnology |
| DOI | 10.1093/jimb/kuab057 |
| 项目映射 | M3（菌株设计靶点）/ B1（菌株-表型知识库）/ D（设计原则写入README） |

## 1. 一句话核心
综述了微生物发酵法生产L-丙氨酸的代谢工程策略，重点介绍 Dr. Lonnie Ingram 团队基于"生长耦联 + 代谢进化"策略构建的 E. coli XZ132（114 g/L、0.95 g/g 葡萄糖、>99.5% 光学纯度），该菌株已授权安徽华恒生物于 2012 年实现商业化，是全球首个以厌氧发酵工业化生产氨基酸的案例（两条产线、2.3 万吨/年、250 m³ 发酵罐）。

## 2. 方法要点（详细）
- **两条生产路线对比**：(A) 酶法——利用 L-天冬氨酸-β-脱羧酶的固定化细胞/细胞悬液对石油基 L-天冬氨酸脱羧，收率>90%；(B) 发酵法——以可再生糖为原料的微生物发酵（更符合工业化与绿色需求）。
- **天然合成途径**：① 转氨酶途径（丙酮酸+谷氨酸/缬氨酸转氨，产生 DL-丙氨酸，无实用价值）；② NAD⁺-依赖的 L-丙氨酸脱氢酶（ALD，由 alaD 基因编码，丙酮酸+氨直接合成 L-丙氨酸，存在于 Arthrobacter oxydans、Bacillus sphaericus、Clostridium sp. P2 等）。
- **代谢工程通用策略**：异源表达 alaD（来源：B. sphaericus、Arthrobacter sp. HAP1、Geobacillus stearothermophilus）；敲除竞争途径基因（ldhA、aceEF、pfl、pps、poxB、mgsA、dadX、ackA、adhE、frdA、alr）；两阶段/两相发酵（好氧生长→厌氧/限氧产酸）；热调控基因开关（cIts857-pR-pL-alaD，33℃生长+1h 42℃热诱导+42℃限氧产酸）；厌氧发酵+代谢进化（177 代，XZ132）。
- **XZ132 的设计逻辑**：用 G. stearothermophilus alaD 替换内源 D-乳酸脱氢酶，删除 mgsA（改善生长）与 dadX（提高手性纯度），使 L-丙氨酸成为唯一发酵产物；厌氧下 L-丙氨酸合成是氧化糖酵解产生的 NADH 的唯一途径，从而把 L-丙氨酸合成与细胞生长强制耦联，形成生长选择压力；全部外源基因染色体整合，无需抗生素与诱导剂，并适应了无机盐培养基。

## 3. 关键结果与指标
- **E. coli XZ132**（E. coli W 底盘，∆pfl ∆ackA ∆adhE ∆mgsA ∆dadX，ldhA::alaD）：**114 g/L L-丙氨酸，0.95 g/g 葡萄糖，>99.5% 光学纯度**，48 h，无机盐培养基批次发酵。
- **E. coli B0016-060BC**（热调控开关）：**120.8 g/L，0.88 g/g**，40 h。
- **E. coli ALS929(pTrc99A-alaD)**（∆pfl ∆pps ∆aceEF ∆poxB ∆ldhA）：两相批次 34 g/L（0.86 g/g）；两相补料 88 g/L（得率接近理论最大值）。
- **C. glutamicum ∆ldhA∆ppc∆alr + alaD + gapA**（30 mM 丙酮酸）：98 g/L，0.83 g/g，>99.5% 光学纯度。
- **C. glutamicum AL107**：71 g/L，0.36 g/g，>99% 光学纯度（限氧）。
- **Lactococcus lactis**（∆ldhA、∆alr）：13 g/L，0.70 g/g，85–90% 光学纯度。
- **Arthrobacter sp. DAN-75**（敲除丙氨酸消旋酶）：75.6 g/L L-丙氨酸，97% 光学纯度，120 h，0.16 g/g（低得率）。
- **商业化**：XZ132 授权华恒生物（AHB），2012 年起实现全球首个发酵法 L-丙氨酸商业化；现两条产线年产能 23,000 吨；250 m³ 发酵罐产量与 5 L 罐一致；L-丙氨酸是首个厌氧发酵工业化生产的氨基酸，发酵法产品占市场份额>60%。

## 4. 数据与代码可用性
未提供（综述论文，无数据集/代码仓库）。文章为开放获取（CC BY 4.0，Oxford University Press）。

## 5. 对我们项目的可借鉴点（重点）
1. **生长耦联选择策略（XZ132 范式）**：将目标产物合成与 NADH 氧化/细胞生长耦联，再用代谢进化（177 代）筛选高产株。这一"生长耦联"思想可直接转化为我们 AI 菌株设计模块（M3）中可计算的打分特征（growth-coupled production），用于 β-丙氨酸/L-高丝氨酸菌株的理性设计与进化实验设计。
2. **完整基因敲除清单即 CRIPSR 靶点先验**：本文汇总的 ldhA、aceEF、pfl、pps、poxB、mgsA、dadX、ackA、adhE、frdA、alr 等竞争途径基因，可作为我们 AI-CRISPR gRNA 效率/靶点选择模块（M1）的目标基因优先级先验知识，也可作为 CRISPRi 敲低实验的候选靶点集。
3. **"生长-生产"两相/热调控发酵范式**：33℃/42℃ 热开关（B0016-060BC）说明动态分离生长与产酸可大幅提高产量；可与我们 LLM-Agent 生成的发酵工艺方案结合，作为菌株设计目标函数中的工艺约束。
4. **手性纯度相关基因（dadX、alr）的删除**提示菌株设计不仅要关注产量，还要关注光学纯度/副产物，可作为设计目标的多目标优化项。
5. **工业化指标三要素**：titer（g/L）、yield（g/g）、productivity（g/L/h）是评估菌株的统一指标；表 1 全部菌株的基因型-表型数据可结构化入库，作为菌株设计模型的验证集/训练标注。

## 6. 与我们方案的冲突/差异点
- 本文为纯代谢工程综述，不涉及 AI/CRISPR 计算设计，与我们的 AI-CRISPR 模块互补而非冲突。
- 厌氧发酵 + NADH 耦联策略依赖"L-丙氨酸是唯一 NADH 汇"这一特殊设计；β-丙氨酸/L-高丝氨酸合成途径的氧化还原需求（NADPH）与 L-丙氨酸不同，该策略不能直接照搬，需重新设计辅因子耦联。
- 多数菌株用质粒+IPTG 诱导体系，与项目"染色体整合、无诱导剂"的工业取向有差异（XZ132 是例外，其全染色体整合、无诱导剂的设计更贴合我们的目标）。

## 7. 行动项建议
- 将表 1 全部菌株的（基因型操作 × 发酵模式 × titer/yield/productivity/光学纯度）结构化录入 knowledge_base（B1），作为菌株设计模型验证集。
- 将"生长耦联"转化为 M3 菌株设计模块的可计算特征（如基于 GEM 的 coupling score），并在 README 中写入该设计原则。
- 将 ldhA/aceEF/pfl/pps/poxB/mgsA/dadX 等竞争途径基因清单纳入 M1 gRNA 靶点库，供 CRISPRi 敲低实验使用。
