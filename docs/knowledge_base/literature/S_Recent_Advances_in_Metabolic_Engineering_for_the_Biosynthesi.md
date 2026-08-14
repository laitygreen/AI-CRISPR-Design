---
# 文献卡：Recent Advances in Metabolic Engineering for the Biosynthesis of Phosphoenol Pyruvate–Oxaloacetate–Pyruvate-Derived Amino Acids（PEP-草酰乙酸-丙酮酸衍生氨基酸生物合成的代谢工程研究进展）

| 字段 | 内容 |
|---|---|
| 分级 | S |
| 主题 | T5 细胞工厂 |
| 年份 | 2024 |
| 期刊 | Molecules |
| DOI | 10.3390/molecules29122893 |
| 项目映射 | M3（菌株设计规则与靶点）/ B1（大规模菌株策略数据库）/ B2（in silico knockout 模拟）/ D（README引用） |

## 1. 一句话核心
全面综述以 PEP-草酰乙酸-丙酮酸（POP）节点为枢纽的 7 种氨基酸（L-Trp、L-Tyr、L-Phe、L-Val、L-Lys、L-Thr、L-Ile）在 E. coli 与 C. glutamicum 中的代谢工程研究进展，以两张大型表格汇总上百个工程菌株的 titer/yield/productivity 数据，系统梳理"解除反馈抑制、碳流优化、转运工程、副产物消除、辅因子工程、动态调控/高通量筛选"六类策略，并前瞻性提出 CRISPR-dCpf1 动态解耦生长-生产、TCA 非依赖辅因子再生与 CO₂ 再利用等方向。

## 2. 方法要点（详细）
- **POP 节点酶学与调控**：E. coli 中 PEP→OAA 由 PEP 羧化酶（PEPC）催化；苹果酸酶两个同工酶 maeB（NADP）与 sfcA（NAD）；PEP 合成酶（ppsA）与 PEP 羧激酶（pckA）负责回补。C. glutamicum 另有 PYR 羧化酶与 OAA 脱羧酶，PYR 羧化酶贡献约 90% 的 OAA 生成。调控：天冬氨酸/苹果酸抑制 PEPC、乙酰-CoA/果糖-1,6-二磷酸激活；FruR 激活 ppsA/pckA 并抑制 pykF；Crp 抑制 pckA；葡萄糖阻遏 pckA/ppsA/maeB/sfcA 表达。
- **策略框架（每氨基酸 4–6 类）**：核心途径改造（抗反馈突变体如 aroGfbr、trpEfbrD、thrAfbr、ilvBNfbr）、POP 节点与 PPP 碳流优化（tktA/ppsA/pckA 过表达、PTS 删除+glf/glk 或 galP、磷酸酮醇酶）、转运工程（YddG/rhtC/thrE/rhtA23/BrnFE/ygaZH、导入子删除）、副产物消除（Δpta/ΔackA/ΔpoxB/ΔldhA、乙醛酸循环改造）、辅因子工程（PPP、pntAB、gapN 替换、NADH 型脱氢酶交换）、HTS 与动态调控（核糖开关、生物传感器、CRISPRi/CRISPR-dCpf1、温度开关、ALE）。
- **表 1（糖酵解衍生：L-Trp/L-Tyr/L-Phe）与表 2（TCA 衍生：L-Val/L-Lys/L-Thr/L-Ile）** 按"菌株 × 工程策略 × 培养方式 × titer × yield × productivity × 参考文献"结构化汇总全部代表菌株。

## 3. 关键结果与指标
- **L-Trp**：E. coli T13 53.65 g/L（0.238 g/g）；TRTH03（+pck/citT/acnBA/icd/pyc 整合）49 g/L（0.19）；SX11（磷酸酮醇酶+glf/glk+ΔpykF）41.7 g/L（0.227，1.04 g/L/h）；Trp30（核糖开关 HTS，无质粒无添加）42.5 g/L（0.178）；C. glutamicum KY9218 58 g/L（tktA 共扩增，+15%）；fruR 删除 titer+62.5%、yield+52.4%；ptsG 删除后 Hpr 突变 N12S 使转化率+38.0%（0.178 g/g）；仅 3% 的 PEP 可用于芳香族氨基酸合成（PEP 限制是核心瓶颈）。
- **L-Tyr**：**E. coli HGD(M9) 92.5 g/L（0.266 g/g，5 L 补料 62 h，当前最高）**——协同工程（磷酸酮醇酶途径+转运+乙酸途径改造+辅因子工程+ALE 耐酸筛选）；DPD4193 55 g/L（0.3 g/g，200 L）；模块化工程（Juminaga 两模块法）达理论产量 80%（2.6 g/L）；gTME 菌株 rpoA14R 13.8 g/L、2.1 g/L/h；sRNA（anti-tyrR/anti-csrA）S17-1 21.9 g/L（高密度培养）；GXP 系统（E. coli 菌群 + CRISPR/dCas9）从高粱髓水解物获 0.163 g L-Tyr/g 原料。
- **L-Phe**：**E. coli PHE05 80.48 g/L（0.27 g/g，1.68 g/L/h，当前最高）**——途径重建+ALE+转录组鉴定 MarA 提高耐受力；Xllp08 72.9 g/L（0.26，1.4）；xllp1 动态调控（PtyrP-aroK）61.3 g/L（0.22，1.27）；BR-42/pAP-B03 57.63 g/L（1.15，抗噬菌体筛选）；yggG 整合降低乙酸（AJ12741/pHYGG 6.4 g/L）。
- **L-Val**：C. glutamicum BNGECTMDLD/ΔLDH（NADH 偏好 ilvCTM + LeuDH，缺氧补料）**227.3 g/L（0.41 mol/mol，最高）**；E. coli W（ΔilvA ΔlacI + lrp/ygaZH/ilvBNfbrCED）60.7 g/L（2.06 g/L/h）；VAL38（ARTP 诱变+HTS）92 g/L（0.34）；基于 in silico 基因敲除模拟（ΔaceF/ΔpfkA/Δmdh）的 E. coli Val 菌株 7.55 g/L（0.378 g/g）；Lrp 生物传感器驱动 ALE（FACS）titer+25%、副产物-3~4 倍，并发现 UreD-E188*（产物）与 GlxR-T93S（副产物）新突变。
- **L-Lys**：**C. glutamicum ZL-92（非 PTS iolT1/iolT2/ppgK）201.6 g/L（0.65 g/g，5.04 g/L/h，最高）**；JL-6 9Ptac-M gdh 181.5 g/L（3.78）；E. coli LATR11 125.6 g/L（0.59，3.14，近理论值）；C. glutamicum LYS-12 120 g/L（0.55，4）；Lys9（ΔaceE+pyc 突变+ΔalaT/avtA/ldhA/mdh/pck+pntAB）526 mM（0.42，2.69）；pntAB 表达使蔗糖上 L-Lys +300%；NADH 型脱氢酶替换（adh_Pa/asd_Tm/dapB_Ec）+30.7%~36.8%；Ec-dapBC115G,G116C 切换辅因子偏好 117.3 g/L（0.44，2.93）；稀有密码子系统 QD01 ΔtRNA_L2 14.8 g/L。
- **L-Thr**：**E. coli 人工多倍体 TH-103Z 160.3 g/L（当前最高）**；TWF083（thrR 衰减子动态调控 arcA/fadR/cpxR/gadE/pykF）116.62 g/L（0.486，2.43）；TWF044 103.89 g/L（0.72，2.16）；TWF113/pFT24rpa1 热开关（37→42℃）达理论值 124.03%；MDS-205（rhtA23 突变转运体）40.1 g/L（0.40）；rhtA 上游 -1 位 G→A 突变使 MG422 产量从 18.4 升至 36.3 g/L。
- **L-Ile**：**C. glutamicum IWJ001（ppnk+TD+AHAS 扩增）32.3 g/L（最高公开报道）**；YILWΔbrnQ+brnFE 29 g/L（0.24）；ppnk+zwf 共表达 +85.9%（4.1 g/L）；ilvAfbr(V140M-F383A) 对 L-Ile 完全抗性（+55.3%）。
- **结论层面**：三大挑战=分支酶对 PEP/PYR/OAA 底物亲和力不足、产物与生长耦联、动态平衡；**CRISPR-dCpf1** 可在指数早期 IPTG 诱导，通过 crRNA 结合 RBS 抑制 pyk/ppc/aceE/pyc/pck/gltA 表达实现生长-生产解耦（Cpf1 直重复序列仅 ~20 nt，比 Cas9 ~60 nt 更经济）。

## 4. 数据与代码可用性
文中声明"Data sharing is not applicable"（综述，未提供数据集/代码）。开放获取（CC BY 4.0，MDPI）。原始数据需回溯表 1/表 2 对应参考文献。

## 5. 对我们项目的可借鉴点（重点）
1. **表 1/表 2 是现成的大规模"菌株基因型-表型"语料**：上百条（菌株 × 工程操作 × titer/yield/productivity × 发酵模式）记录可直接结构化，作为菌株设计 AI 的训练集（回归/排序）、LLM-RAG 检索语料或 M3 验证集——这是本项目最直接可落地的数据资产。
2. **in silico 基因敲除模拟引导设计（E. coli Val，ΔaceF/ΔpfkA/Δmdh）**：用 GEM 敲除模拟（如 COBRApy 的 OptKnock/最小通量分析）先计算候选靶点再做实验，可作为我们 B2 管线"菌株设计候选生成"模块的标准流程，与 AI-CRISPR 靶点预测互为补充。
3. **CRISPR-dCpf1 动态调控的 crRNA 设计需求**：Cpf1（PAM TTTV，crRNA ~20 nt，可自加工 crRNA 阵列）用于抑制 pyk/ppc/aceE/pyc/pck/gltA 等 POP 节点基因——我们的 gRNA 设计模块（M1）应支持 Cpf1/crRNA 设计（含多靶标阵列组装），并可与 dCas9-CRISPRi 对比评估。
4. **NADPH 供给的通用规则**：L-Val（2 NADPH/分子）、L-Lys（4 NADPH/分子）、L-Thr/L-Ile 均受 NADPH 限制；pntAB、gapN 替换、NADH 型脱氢酶交换是三类通用解法——可编码为菌株设计规则库（M3）中"辅因子平衡"规则，适用于我们的 β-丙氨酸/L-高丝氨酸（每分子高丝氨酸需 2 NADPH）。
5. **生物传感器-HTS-ALE 闭环**（Trp30 核糖开关、Lrp 生物传感器 FACS、pSenLys-Spc 筛选 PCx 突变体）：证明"传感器→筛选→基因组测序→SNP 回补验证"是发现新靶点（如 UreD、GlxR）的有效路径，与我们的 LLM-Agent 实验设计闭环设计理念一致，可写入实验方法论。
6. **PTS 删除 + 非 PTS 摄取（galP/glf/glk/iolT1/iolT2/ppgK）**：节省 PEP（L-Trp 中仅 3% PEP 可用）是芳香族/天冬氨酸家族氨基酸的共同痛点，我们设计 β-丙氨酸/L-高丝氨酸菌株时也应把"PEP 节约"作为可计算约束。
7. **动态/多倍体/基因组精简等系统层面策略**（多倍体 E. coli 160.3 g/L L-Thr、染色体整合替代质粒）提示菌株设计应覆盖基因组层面的特征（拷贝数、染色体整合、多倍体化），可作为设计空间扩展方向。

## 6. 与我们方案的冲突/差异点
- 该综述未覆盖 β-丙氨酸与 L-高丝氨酸本身（仅作为天冬氨酸家族提及），需要从 L-Thr/L-Lys 策略类比迁移，迁移时需注意各氨基酸的反馈调控与外排机制差异。
- 大量数据来自 C. glutamicum（如 PYR 羧化酶占 90% OAA），与我们的 E. coli 底盘存在宿主差异，酶学与调控假设不能直接套用。
- 全文无 AI/深度学习内容；属于系统代谢工程综述，与我们的 AI-CRISPR 计算设计互补。

## 7. 行动项建议
- 从表 1/表 2 抽取全部菌株条目，构建结构化"菌株工程策略数据库"（宿主 × 基因操作 × 培养方式 × titer/yield/productivity × 文献），入库 B1，作为菌株设计模型训练集与 RAG 检索语料。
- 将 in silico 基因敲除模拟（OptKnock/最小通量）加入 B2 管线，输出菌株设计候选基因清单。
- 将 Cpf1 crRNA 设计需求写入 M1 gRNA 设计模块需求文档（PAM TTTV、20 nt crRNA、阵列组装）。
- 将"PEP 节约（PTS→非 PTS）""NADPH 供给三类解法""外排增强"写入 M3 菌株设计规则库。
- 在 README 中引用本综述作为 POP 氨基酸代谢工程策略的权威参考（补料数据与设计规则）。
