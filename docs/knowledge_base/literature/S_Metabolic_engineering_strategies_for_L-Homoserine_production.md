---
# 文献卡：Metabolic engineering strategies for L-Homoserine production in Escherichia coli（大肠杆菌L-高丝氨酸生产的代谢工程策略）

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T5 细胞工厂 |
| 年份 | 2024 |
| 期刊 | Microbial Cell Factories |
| DOI | 10.1186/s12934-024-02623-7 |
| 项目映射 | M3（菌株设计靶点与规则）/ B1（菌株-表型知识库）/ M1（CRISPRi gRNA靶点）/ D（README引用） |

## 1. 一句话核心
系统综述 E. coli 中 L-高丝氨酸的生物合成、分泌（RhtA/RhtB/EamA/BrnFE）与调控（反馈抑制、thrL 衰减、MetJ 阻遏）机制，归纳六类代谢工程策略（解除反馈抑制、恢复葡萄糖摄取、关键节点改造、辅因子平衡、转运改造、大规模靶点识别），汇总当前最高 **110.8 g/L（W-H18/pM2/pR1，0.64 g/g，1.82 g/L/h）** 的补料分批菌株数据，指出 OAA 供给与 NADPH 供给是主要瓶颈；并强调 β-丙氨酸与 L-高丝氨酸同源于天冬氨酸，TCA 优化策略可互相迁移。

## 2. 方法要点（详细）
- **合成途径**：EMP + TCA + L-天冬氨酸途径，三步合成：天冬氨酸激酶（thrA/metL/lysC）→ 天冬氨酸半醛脱氢酶（asd）→ 高丝氨酸脱氢酶（thrA/metL）；每分子天冬氨酸→L-高丝氨酸需 **2 分子 NADPH**（asd 与高丝氨酸脱氢酶均为 NADPH 依赖）；天冬氨酸半醛是天冬氨酸家族（Lys/Thr/Met/高丝氨酸）分支节点。
- **反馈抑制**：AKI（thrA）被苏氨酸抑制；AKIII（lysC）被赖氨酸抑制；NADP⁺-谷氨酸脱氢酶（gdhA）被高丝氨酸抑制。
- **转录调控**：thrLABC 操纵子（thrL 编码 21 aa 前导肽，含 8 个苏氨酸+4 个异亮氨酸调控位点，衰减机制调控）；metL 被 MetJ + S-腺苷甲硫氨酸阻遏；ALE 得到的 thrL* 等位基因可缓解 L-高丝氨酸毒性。
- **六类策略**：
  1. **解除反馈抑制**：thrAfbr（thrAC1034T）、lysCfbr（C1055T）；Ptrc-thrAfbr 三拷贝；敲除 thrB（降低流向苏氨酸）、lysA（减少前体竞争）。
  2. **恢复葡萄糖摄取**：ΔptsG + 过表达 galP（非 PTS 摄取，节省 PEP），不同菌株提升约 19.0%（6.27 g/L）与 400%（4.29 g/L）。
  3. **关键节点改造**：染色体 Ptrc 替换 ppc 天然启动子（H06：7.02 g/L，+11.8%）；基因组整合 Ptrc-aspC + aspA（+5.7%，7.42 g/L）；HOM-7 整合 Ptrc-ppc 拷贝（2.9 g/L，+61.1%）；PfliC 动态调控 thrB（HOM-5：1.8 g/L）；thrB 起始密码子 ATG→GTG。
  4. **辅因子平衡**：过表达 pntAB（NAD(P)转氢酶，NADH→NADPH）：SHL5 1.2 g/L（6 倍）；HOM-11 10.7 g/L（+21.6%）；H24 27.83 g/L（+21.7%）；再加拷贝达 33.77 g/L；或替换为 NADH 依赖脱氢酶：aspB_Pa（P. aeruginosa 天冬氨酸脱氢酶）+ asd_Tm（Titrella mobile 天冬氨酸半醛脱氢酶），Cg13-19 13.3 g/L（+18%）。
  5. **转运系统改造**：Ptrc-rhtA（HS3：2.63 g/L，+30.9%）、Ptrc-eamA（HS4：2.17 g/L）；双拷贝 Trc-rhtA + Trc-eamA（HS5：3.14 g/L，+54.2%）；rhtA23 启动子突变（-1 位 A→G）：pBRmetL-rhtA23 1.81 vs pBRmetL 1.04 g/L；Plpp 强启动子 rhtA（H20：22.86 g/L）；ΔtdcC 促进生产、ΔsstT 无显著效果；外排容量存在上限（再增强 rhtB/brnFE 无效）。
  6. **大规模靶点识别**：CRISPRi（dCas9）与合成 sRNA 文库（122 个 sRNA 抑制尸胺途径相关基因）实现可调、可逆、染色体层面的大规模基因抑制；sgRNA 下调 ptsH、ptsI、crr、ptsG、tktA、rpe、talB、argA、argG、proB、gadA、zwf、pta、poxB 等使 L-高丝氨酸产量提升 50–100%；sRNA 靶向 ackA、pdhR 使尸胺产量提升约 30–40%（表明可发现非显而易见靶点）。
- **TCA/乙醛酸循环优化（与 β-丙氨酸共享策略）**：ΔfumABC 提高延胡索酸（利于 β-丙氨酸通量）；Δmdh 增加 OAA 供给；过表达 icd、下调 odhA 优化谷氨酸供给；IclR 破坏以重定向乙醛酸支路碳流。

## 3. 关键结果与指标
- **表 2 菌株汇总（补料分批，E. coli）**：
  - HM5（b+c+d+e，pBRmetL-pNrhtA）：39.5 g/L，0.29 g/g，0.9 g/L/h
  - LJL12（b+c+e）：35.8 g/L，0.35 g/g，0.82 g/L/h
  - HS33（a+b+c+d+e+f）：37.6 g/L，0.31 g/g，0.35 g/L/h
  - HOM-14（b+c+d+g）：60.1 g/L，0.42 g/g，1.25 g/L/h
  - HS15（b+c+d+e+g）：84.1 g/L，0.5 g/g，1.96 g/L/h
  - **W-H18/pM2/pR1（a+b+c+d+e）：110.8 g/L，0.64 g/g，1.82 g/L/h（最高 titer）**
  - SHL17（b+c+d+g）：44.4 g/L，0.21 g/g，0.93 g/L/h
  - H28（b+c+d+e+g）：85.3 g/L，0.43 g/g，1.78 g/L/h
- **单策略对照**：Ptrc-thrAfbr（HP1）24 h 7.18 g/L vs Ptrc-metL（HP2）5.62 g/L（+27.8%）；thrA 策略产量约为 lysC 策略的 3 倍（HM4 pBRthrAfbr vs pBRlysCfbr）——天冬氨酸半醛→高丝氨酸还原是关键限速步。
- **衍生品**：高丝氨酸→1,3-PDO（0.32 g/L，无需 VB12）；O-乙酰高丝氨酸 OAH 1.68 g/L，MetX 三突变（F147L-M182I-M240A）使 OAH 产量 +57.14%。
- **相关 β-丙氨酸参照**：Xu et al. 用多变量模块代谢工程（MMME）实现 β-丙氨酸补料分批 **37.9 g/L**。

## 4. 数据与代码可用性
文中声明："No datasets were generated or analysed during the current study"（综述，未提供数据集/代码）。许可：CC BY-NC-ND 4.0。

## 5. 对我们项目的可借鉴点（重点）
1. **与 β-丙氨酸同源于天冬氨酸 → 策略直接迁移**：ΔfumABC（延胡索酸→β-丙氨酸通量）、Δmdh/过表达 icd/下调 odhA（OAA 与谷氨酸供给）等 TCA 优化策略明确标注"可应用于 β-丙氨酸"——应直接纳入我们 β-丙氨酸菌株设计规则库。
2. **CRISPRi/sRNA 大规模靶点识别 = 我们 M1 gRNA 设计模块的直接应用场景**：本文列举的 14 个 sgRNA 靶点（ptsH、ptsI、crr、ptsG、tktA、rpe、talB、argA、argG、proB、gadA、zwf、pta、poxB）可立即作为 gRNA 效率预测模型的候选测试集，并开展 dCas9-CRISPRi 实验验证"AI 预测→实验闭环"。
3. **NADPH 瓶颈的三条解决路线**（pntAB 转氢酶、NADH 型脱氢酶替换 aspB_Pa/asd_Tm、动态调控）可作为菌株设计模块（M3）的可计算特征/规则（如"若产物合成每步消耗 NADPH，则建议过表达 pntAB"）。
4. **外排工程细节**：rhtA23 启动子突变（-1 位 A→G）、Plpp 强启动子、双拷贝 rhtA+eamA 的量化效果（+54.2%）可直接指导我们 L-高丝氨酸菌株的转运改造；"外排容量饱和"提示需组合其他策略。
5. **动态调控范式（PfliC 自调控启动子、thrB 弱化避免营养缺陷）**：与我们的 LLM-Agent 发酵工艺/动态调控方案设计结合，作为菌株设计的约束条件。
6. **表 2 的 8 株菌株数据（titer/yield/productivity × 策略组合）** 是现成的结构化训练/验证集，可建立"策略组合→产量"的回归/排序模型（为菌株设计 AI 提供监督信号）。
7. **MMME 多变量模块代谢工程（β-丙氨酸 37.9 g/L）** 的模块划分思想（PEP-OAA/FUM-ASP 模块与 ASP-HOM 模块）可用于我们 β-丙氨酸/L-高丝氨酸双产物菌株的分模块设计与优化。

## 6. 与我们方案的冲突/差异点
- L-高丝氨酸对宿主有毒性（胞内积累抑制生长），β-丙氨酸的毒性机制不同，各自需要专门的耐受设计（ALE、传感器筛选），不能混用同一耐受策略。
- 综述不涉及 AI/CRISPR 计算设计（仅提到 CRISPRi 作为实验工具），与我们 AI-CRISPR 部分互补。
- 部分策略依赖 C. glutamicum 结果（如 BrnFE 源基因），宿主迁移需验证。

## 7. 行动项建议
- 将表 2 的 8 株菌株（策略组合 × titer/yield/productivity）结构化录入 B1，作为 M3 菌株设计模型验证集。
- 将 CRISPRi 靶点列表（ptsH/ptsI/crr/ptsG/tktA/rpe/talB/argA/argG/proB/gadA/zwf/pta/poxB）纳入 M1 gRNA 设计候选库，设计 dCas9-sgRNA 并规划 CRISPRi 实验。
- 将 pntAB/NADH 型脱氢酶替换、fumABC/mdh/icd/odhA TCA 优化、rhtA23/Plpp 外排工程写入菌株设计规则库（M3 规则文件）。
- 在 README 中新增"L-高丝氨酸代谢工程策略汇总"章节并引用本综述。
