# 方法学习包 · 总索引（GitHub 生信方法全攻略）

> 版本 v1.0 | 日期 2026-08-14 | 用途：将知识库涉及的生信方法全部落地为可复用代码学习包
> 结构：5 条路线 ×（公共数据库原件 + 生信处理代码 + 大模型训练代码 + 解释文档），多途径方法分路线

---

## 路线总览

| 路线 | 方法包文档 | 对应模块 | 本地仓库（GitHub 原件） | 多途径方法 |
|---|---|---|---|---|
| A | [RouteA_gRNA效率预测方法包.md](RouteA_gRNA效率预测方法包.md) | M1 | DeepCRISPR、CRISPRon、Azimuth | A-1 旧版TF1复现 / A-2 现代PyTorch重实现 |
| B | [RouteB_脱靶预测方法包.md](RouteB_脱靶预测方法包.md) | M2 | CRISPR-Net、DeepCRISPR | B-1 规则评分(CFD) / B-2 CNN / B-3 DNABERT-Epi |
| C | [RouteC_DNA预训练模型方法包.md](RouteC_DNA预训练模型方法包.md) | M1底座 | DNABERT、DNABERT-2、Nucleotide Transformer、HyenaDNA | R0选型基准 / R1冻结嵌入 / R2 LoRA微调 / R3长上下文 |
| D | [RouteD_LLM与Agent方法包.md](RouteD_LLM与Agent方法包.md) | M3/M4 | BioGPT(microsoft)、BioT5(QizhiPei)、CRISPR-GPT(cong-lab) | D-1 LoRA微调 / D-2 RAG问答 / D-3 Agent编排 |
| E | [RouteE_代谢网络与多组学方法包.md](RouteE_代谢网络与多组学方法包.md) | B2/B3 | cobrapy、breseq、CRISPResso2 | FBA/pFBA/FVA / WGS变异 / 编辑效率 / RNA-seq |

## 本地仓库原件（methods/repos/，11 个）

| 仓库 | 来源 | 用途 |
|---|---|---|
| DeepCRISPR-master | bm2-lab/DeepCRISPR | gRNA效率+脱靶统一框架（TF1） |
| crispron-main | RTH-tools/crispron | gRNA效率预测（PyTorch，含6预训练模型） |
| Azimuth-master | MicrosoftResearch/Azimuth | Doench 2016 评分模型+V1/V2数据 |
| CRISPR-Net-master | JasonLinjc/CRISPR-Net | 脱靶 RCNN 模型+数据 |
| DNABERT-master | jerryji1993/DNABERT | k-mer DNA 预训练底座 |
| DNABERT_2-main | MAGICS-LAB/DNABERT_2 | BPE 多物种底座（含 LoRA 微调） |
| nucleotide-transformer-main | instadeepai/nucleotide-transformer | NT-v1/v2 底座（JAX） |
| hyena-dna-main | HazyResearch/hyena-dna | 长上下文底座 |
| cobrapy-devel | opencobra/cobrapy | FBA/pFBA/FVA 约束建模 |
| breseq-master | barricklab/breseq | ALE 变异解析 |
| CRISPResso2-master | pinellolab/CRISPResso2 | 编辑效率分析 |

## 外部资源速查（需联网/注册）

| 资源 | 链接 | 用途 |
|---|---|---|
| BiGG iML1515 模型 | bigg.ucsd.edu | E. coli 代谢网络模型（FBA） |
| EcoCyc | ecocyc.org | E. coli 通路数据库（需注册） |
| RegulonDB | regulondb.ccg.unam.mx | 转录调控数据库 |
| NCBI MG1655 | NC_000913.3 | 参考基因组 |
| HuggingFace DNABERT-2 | huggingface.co/zhihan1996 | 预训练权重 |
| CRISPOR | crispor.tefor.net | gRNA 设计聚合工具 |
| rth.dk CRISPRon 数据 | rth.dk/resources/crispr | 23902 训练数据（需查证申请方式） |

## 下一步建议（结合备赛时间线）

1. **P0（本周）**：按 RouteA §2 命令链跑通 CRISPRon 推理（`bash bin/CRISPRon.sh test/seq.fa`），验证环境
2. **P0**：按 RouteC §3 骨架加载 DNABERT-2，跑通 embedding 提取（mean pooling）
3. **P1（9 月初）**：构建 E. coli gRNA 数据集，按 RouteA §3 训练 PyTorch 版效率模型
4. **P1**：按 RouteE §2 用 cobrapy 加载 iML1515 跑 FBA，识别 β-丙氨酸/高丝氨酸瓶颈
5. **P2**：RouteD LLM RAG 知识库搭建 + RouteB DNABERT-Epi 脱靶增强

---

## 质量说明

- 文档内容全部来自本地仓库真实代码 + 文献卡实测数据，未编造；无法确认处均标注'需查证'
- 代码块采用 4 空格缩进（规避反引号传输问题），在常见 Markdown 渲染器正常显示
- 部分仓库为 TF1/JAX 旧框架，运行时需 Docker 或适配（文档已标注）

