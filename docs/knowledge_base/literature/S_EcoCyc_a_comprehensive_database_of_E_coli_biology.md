# 文献卡：EcoCyc: fusing model organism databases with systems biology

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T6 生信管线（数据库） |
| 年份 | 2013 |
| 期刊 | Nucleic Acids Research (41:D605-D612) |
| DOI | 10.1093/nar/gks1027 |
| PMC | PMC3531154 |
| 项目映射 | B1（靶基因功能注释）、B2（代谢通路与调控数据源）、B3（基因-表型知识）、M3（LLM RAG 知识库） |

## 1. 一句话核心
EcoCyc 是 E. coli K-12 的综合性模型生物数据库，融合基因组注释、代谢通路（PathoLogic 推断）、调控网络、转运与信号转导，并提供 Pathway Tools 软件实现通路的计算推断与可视化——是代谢工程靶点注释与通路分析的核心数据源。

## 2. 方法要点（详细）
- 数据库内容：基因组（~4,500 基因注释）、代谢网络（~1,500 代谢物、~2,400 反应、~200 通路，经 PathoLogic 从基因组自动推断）、调控（转录因子-靶基因、调控网络）、转运蛋白、生长条件
- 数据整合：从 BioCyc 家族自动生成，与其他 BioCyc 数据库共享框架；用户可下载 flat files / BioPAX / SBML 格式
- 工具：Pathway Tools（通路推断、Flux 分析、比较基因组）、EcoCyc 网页查询、EcoCyc API（SmartTables、cyto-views）
- 关联资源：与 RegulonDB、UniProt、NCBI 等交叉链接

## 3. 关键结果与指标
- 覆盖 E. coli K-12 MG1655 全基因组（~4,500 蛋白编码基因，其中 ~1,500 有实验证据的基因功能）
- 代谢通路推断：PathoLogic 在 E. coli 上通路覆盖率高（文中报告多个通路重建评估）
- 数据库持续更新（最新版含更多实验支持的调控与转运数据）

## 4. 数据与代码可用性
- 官网：https://ecocyc.org （免费学术使用，需注册）
- 下载：flat files、BioPAX、SBML、Pathway Tools 软件
- API：EcoCyc Web API / SmartTables 用于程序化访问
- PDF 获取：PMC3531154（https://pmc.ncbi.nlm.nih.gov/articles/PMC3531154/）需手动下载（OUP 反爬）

## 5. 对我们项目的可借鉴点
1. **B1 靶点注释数据源**：用 EcoCyc 的基因-通路-反应注释为全基因组 gRNA 扫描结果做功能标注，优先靶向代谢通路基因而非未知功能基因
2. **B2 代谢瓶颈识别**：结合 iML1515 FBA 与 EcoCyc 通路图，快速定位 β-丙氨酸/高丝氨酸合成通路（天冬氨酸家族）的关键节点与竞争分支
3. **M3 LLM RAG 知识库**：将 EcoCyc 的基因功能、通路描述、调控关系整理为结构化文本语料，供 LLM 检索增强（回答为何改造 panD/aspC 时引用权威注释）
4. **B3 基因-表型先验**：EcoCyc 的基因必需性与通路冗余信息作为靶点选择的先验约束（避免敲除必需基因）

## 6. 与我们方案的冲突/差异点
- 本项目以发酵工程应用为主，EcoCyc 偏数据库与通路推断，需结合 GEM（iML1515）做定量通量分析，二者互补不冲突

## 7. 行动项建议
- 生信组：注册 EcoCyc 学术账号，下载 flat files，建立基因-通路映射表（8/25 前）
- 模型组：将 EcoCyc 基因描述清洗为 RAG 语料（9/5 前）
- 修正记录：原文献库中 EcoCyc 条目 DOI 已从错误的 gky1058 修正为 gks1027；PDF 需从 PMC3531154 手动获取

