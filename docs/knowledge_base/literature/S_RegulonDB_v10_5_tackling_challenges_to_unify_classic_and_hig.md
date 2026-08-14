---
# 文献卡：RegulonDB v10.5: tackling challenges to unify classic and high throughput knowledge of gene regulation in E. coli K-12

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T3 DNA底座（转录调控数据库/知识库） + T6 生信管线（多组学整合） |
| 年份 | 2019 |
| 期刊 | Nucleic Acids Research, Vol. 47, Database issue, D212–D220 |
| DOI | 10.1093/nar/gky1077 |
| 项目映射 | D（数据库资源，直接可用）；M3（DNA底座：调控区域定义、TFBS、生长条件本体）；B2（ChIP+RNA-seq 整合管线范本） |

## 1. 一句话核心
RegulonDB v10.5 在 20 年经典分子生物学文献精选基础上，新增高通量（HT）数据精选（gSELEX、ChIP-seq/exo）、生长条件本体 MCO、GENSOR Units 代谢-调控整合和 BioNLP 半自动精选，首次给出大肠杆菌 K-12 转录调控网络规模的定量估计（全基因组约 4.6 万条 TF–基因互作，已知约 10%，其中约 1.3 万条真正参与转录起始调控）。

## 2. 方法要点（详细）
- **经典文献精选**：每月按关键词（转录、基因调控）收集文献，经 EcoCyc capture forms 精选后同步写入两个数据库（数据完全一致）。
- **HT 数据精选与处理管线（半自动）**：从 GEO 下载数据（SOFT 文件元数据）；RNA-seq 用 RPKM/FPKM/RPM 汇总，TF 结合实验用 ChIP-exo/ChIP-seq 强度值；坐标统一转换到 NC000913.3（ECOCYC map-seq-coords 工具）；用 **macs2 + BEDOPS** 找富集区域 → **RSAT matrix scan** 找候选 TFBS → 与 RegulonDB 已知 TFBS 重叠 >50% 判定同一；RNA-seq 两组条件做双样本 t 检验 + FDR 校正（volcano plot，FDR<5% 为差异基因）；调控区域定义为"该 TF 已知最远 TFBS 的距离"或"转录起始位点 −400 到 +100 bp"区间。
- **MCO（Microbial Conditions Ontology）**：受控词表描述实验可复现的最小属性集：Genetic background（Organism/Strain/Substrain/Genotype）、Medium、Medium supplements、Aeration、Temperature、pH、Pressure、OD、Growth phase、Growth rate、Vessel、Agitation、Genome version、实验技术；形成"GC phrases"→ 对比生成"contrasts"（识别实验变量）。
- **GENSOR Units 组装**：以每个 TF 为中心，自动检索其效应物、活/非活构象、受调基因、RI 效应（RegulonDB）+ 受调基因产物、酶催化反应、底物产物（EcoCyc）+ 异源多聚体复合物成员 + Complementary Pathway Reactions（同通路代谢物间连通的补充反应，不再限 3 步中间反应）；CellDesigner v4.4 自动绘图 + 人工编辑。
- **BioNLP 研究**：用 NLP 从文献自动提取生长条件对比变量；用人工 TF 摘要训练自动摘要器（分类 TF 结构域与调控过程相关句子）；提供精选句子数据集供 BioNLP 社区做分类/段落检测/关系抽取。

## 3. 关键结果与指标
- **网络规模估计**：207/约 300 个 TF（69%）有至少 1 个结合位点证据；4,358 条 TF–基因互作影响 1,823 个基因；CRP 影响 522 个基因；连接度服从幂律分布；HT 数据显示平均互作数增加约 7 倍（精选后约 2 倍）→ 估计全基因组上限约 45,759 条 TF–基因互作，即当前知识覆盖约 9.5%；其中约 13,000 条明确参与转录起始调控，已知约 1/3。
- **HT 精选**：约 51 篇 HT 文献 → 9 个 TF 的 1,048 条新 RI + 107 条已知 RI；另有 36 个 TF/σ 因子的 16,609 条"interactions"以数据集形式提供（无调控证据）。
- **初步整合管线（proof of concept）**：5 个 GEO 系列、32 个样本（Fur、Cra、OxyR、SoxR、GadE、GadW、GadX、OmpR；ChIP-exo/chip/seq + RNA-seq/芯片）→ 识别 4,780 条 RI，其中 161 条已收录。
- **Cra 实例**：经典实验 79 个 Cra 调控基因；HT 在果糖/葡萄糖/乙酸三种条件下发现 338 个新调控基因且条件间重叠少；KEGG 富集显示 TCA 与乙醛酸循环在果糖和乙酸富集（P<0.05），糖酵解在乙酸和葡萄糖富集——代谢与调控连接复杂。
- **MCO 规模**：40 篇经典 + 9 篇 HT 文献、49 个 GEO 实验的 GC 注释；378 条 GC phrases、269 个 contrasts、164 个 controls、256 个 tests、162 个 variables；73 个基因和 4,059 条 RI 关联了 GC 影响。
- **GENSOR Units**：200 个 TF（新增 16 个：BCCP、BtsR、CecR、HigA、HigB-HigA、HprR、MraZ、NimR、PdeL、RclR、SrlR、SutR、TtdR、UvrY、YhaJ、YjjQ）；86 个 Unit 新增 310 条代谢物-酶互作；>145 条 complementary pathway reactions（50% 仅 1 步中间反应，最长 13 步）；70 个 Unit 写出分子生物学 + 生理学双摘要。
- 58% 受调基因具有多个 TF 结合位点——组合调控普遍。

## 4. 数据与代码可用性
- RegulonDB：http://regulondb.ccg.unam.mx/（免费浏览/下载；Downloads 菜单可按字段过滤 HT 数据集；JBrowse 可视化轨道；MCO browser）。
- 与 EcoCyc 共享精选数据（https://biocyc.org/ECOLI/）；许可未明确列出（开放获取 CC BY-NC 4.0）。
- 管线所用工具均开源：macs2、BEDOPS、RSAT、CellDesigner。

## 5. 对我们项目的可借鉴点（重点，结合大肠杆菌氨基酸细胞工厂 + AI-CRISPR 设计）
1. **调控区域的定义可直接用于 gRNA 靶向位点设计（M3/M1）**：RegulonDB 的"-400/+100 bp 相对转录起始位点"调控区域定义和已知 TFBS 集合，可作为我们 CRISPR 干扰（CRISPRi）/基因编辑 gRNA 设计时"必须命中/必须避开"的注释层——例如在 β-丙氨酸/L-高丝氨酸通路基因的启动子区设计 gRNA 时，优先选择不与关键 TF（CRP、Cra、FNR 等）结合位点重叠的位置，避免干扰全局调控。
2. **TF–基因互作 + 生长条件本体（MCO）为实验设计提供约束**：MCO 的受控词表（培养基、碳源、OD、生长期、温度、pH）可直接复刻为我们的发酵实验元数据 schema——不同碳源/诱导条件下菌株转录组可比性依赖条件标准化；这也是多组学数据集（B3）对齐的前提。
3. **ChIP+RNA-seq 整合判 RI 的管线可迁移为"gRNA 编辑效果评估"管线（B2）**：macs2 peak → 结合位点 → 与差异表达（FDR<5%）联合推断"结合是否影响表达"，正是我们评估 CRISPR 敲除/抑制靶点后"结合-表型"因果性的统计框架（如验证 gRNA 是否真的抑制了目标通路基因）。
4. **GENSOR Units 的代谢-调控整合图可作为细胞工厂改造的"全局扰动地图"（T5）**：以 TF 为中心的信号→调控→代谢反应网络，可用来预测在 β-丙氨酸通路中过表达/敲除某个基因时，上游转录因子（如 Cra 受 FBP 别构调控）会如何重新分配碳通量——为我们的"改造位点选择 + 补偿策略"提供先验。
5. **规模估计方法（约 7 倍外推）提醒我们训练数据覆盖度评估**：如同 RegulonDB 估算网络完整度（9.5%），我们的 gRNA 训练集也应评估覆盖度（如目标基因启动子空间/序列空间采样率），避免模型在未覆盖区域失效。

## 6. 与我们方案的冲突/差异点
- RegulonDB 聚焦转录起始调控（prokaryotic），我们的系统还需整合翻译水平、蛋白水平调控与代谢物反馈抑制，单靠 RegulonDB 无法覆盖完整调控图景（需补充 EcoCyc 代谢/酶调控数据）。
- HT 数据（ChIP-seq）中大量结合位点与表达变化无关（无调控证据），直接用作训练标签会引入噪声——我们做 gRNA 靶点-表型标签时应区分"结合"与"功能"证据等级（RegulonDB 的 RI vs interaction 分级思路）。

## 7. 行动项建议
- **纳入训练集/知识库（D）**：将 RegulonDB v10.5 的 TFBS、启动子、调控区域注释下载入库，作为 M1 gRNA 靶点设计的约束特征与 M3 DNA底座的注释层。
- 采用 MCO 词表作为发酵实验元数据模板，写入 README 或数据规范文档（B3 数据集标准）。
- 复现其"peak + 差异表达联合推断"统计流程（macs2 + t-test/FDR + −400/+100 区域映射），作为 gRNA 编辑效果评估子模块（B2）基线。
- 将 GENSOR Unit 的 TF-中心网络用于 β-丙氨酸/L-高丝氨酸通路改造的扰动模拟（T5 先验知识）。
