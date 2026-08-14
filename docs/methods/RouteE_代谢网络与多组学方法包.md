# RouteE 代谢网络与多组学方法包

## 0. 路线总览

本路线解决"改造后菌株到底改得对不对、通量走向哪、哪些基因该敲/该增"三类问题，是"AI-CRISPR 驱动大肠杆菌氨基酸细胞工厂智能设计"的验证与机理闭环：AI 选出 gRNA 靶点后，需要代谢网络建模给出通量层面的设计依据，需要 WGS/编辑效率分析确认"编辑是否成功、有无意外突变"，需要 RNA-seq 确认转录层面的真实扰动。四块子任务相互独立、可并行：

| 子路线 | 工具 | 回答的问题 |
|---|---|---|
| E1 代谢网络建模 | cobrapy + iML1515（FBA/pFBA/FVA） | 敲除/过表达某基因后通量如何重分配；哪些基因必需/低效/冗余（靶点优先级计算依据） |
| E2 WGS 变异解析 | breseq + gdtools | 传代/编辑后基因组出现哪些 SNP/缺失/插入/扩增（含意外突变） |
| E3 编辑效率分析 | CRISPResso2 | 目的位点编辑效率、等位基因谱、脱靶污染 |
| E4 转录组差异分析 | DESeq2 | 改造前后/敲除 vs 对照的差异表达与通路重编程 |
| E5 数据库资源 | EcoCyc / RegulonDB / BiGG(iML1515) | 靶点注释、调控区域约束、GEM 模型获取 |

## 1. 公共数据库与资源原件

| 数据/模型/工具 | 来源 | 获取方式 | 用途 | 注册/授权 |
|---|---|---|---|---|
| iML1515（E. coli GEM，2712 基因/4056 反应/1877 代谢物） | BiGG 数据库 | https://bigg.ucsd.edu/models/iML1515（SBML/JSON/MAT/YAML 下载）；或 cobra.io.load_model("iML1515") 在线拉取 | FBA/pFBA/FVA 的模型底座 | 免费，下载需注册 |
| e_coli_core / textbook（入门小模型） | BiGG / cobrapy 内置 | cobra.io.load_model("e_coli_core") | 跑通管线、教学调试 | 否 |
| EcoCyc（约 4500 基因、约 2400 反应、约 200 通路注释） | EcoCyc 官网 | https://ecocyc.org（flat files / BioPAX / SBML 下载） | 基因-通路-反应注释、通路图、靶点注释 | 学术免费，需注册 |
| RegulonDB v10.5（TFBS、启动子、调控区域、MCO 本体） | RegulonDB | http://regulondb.ccg.unam.mx/（Downloads 菜单） | gRNA 靶向位点的"必须命中/必须避开"注释层（调控区域约 -400/+100 bp） | 免费浏览/下载（CC BY-NC 4.0） |
| E. coli MG1655 参考基因组（NC_000913.3） | NCBI GenBank | https://www.ncbi.nlm.nih.gov/nuccore/NC_000913.3（gbk/fna） | breseq 比对参考、CRISPResso2 参考 | 否 |
| breseq（变异解析管线） | GitHub barricklab/breseq | 本地 methods/repos/breseq-master；conda install -c bioconda breseq | WGS 变异检测 | 开源 GPL |
| CRISPResso2（编辑效率） | GitHub pinellolab/CRISPResso2 | 本地 methods/repos/CRISPResso2-master；pip install CRISPResso2 或 bioconda | 编辑效率/等位基因分析 | 开源 GPL |
| cobrapy（约束建模） | GitHub opencobra/cobrapy | 本地 methods/repos/cobrapy-devel；pip install cobra | FBA/pFBA/FVA 实现 | 开源 LGPL/GPL |
| DESeq2 | Bioconductor | https://www.bioconductor.org/packages/release/bioc/html/DESeq2.html | RNA-seq 差异分析 | 开源 |
| 进化 E. coli 多组学数据（50 套蛋白组+转录组，pFBA 验证用） | UCSD / ProteomeCommons | 见文献卡 A_Omic_data...（http://systemsbiology.ucsd.edu/In_Silico_Organisms/E_coli/E_coli_expression2） | 模型-组学一致性基准 | 开源 CC BY-NC-SA |

> 需查证：BiGG 在线 load_model 对 iML1515 的网络直连在国内网络下是否稳定，建议提前下载 SBML 存本地，用 cobra.io.read_sbml_model("iML1515.xml") 读取。

## 2. 生信处理代码参考

### 2.1 代谢网络建模（cobrapy，本地仓库 methods/repos/cobrapy-devel）

核心源码位置与 API：

- FBA：src/cobra/flux_analysis/ 导出；用法见 documentation_builder/simulating.ipynb
- pFBA：src/cobra/flux_analysis/parsimonious.py → cobra.flux_analysis.pfba(model, fraction_of_optimum=1.0, objective=None, reactions=None)
- FVA：src/cobra/flux_analysis/variability.py → cobra.flux_analysis.flux_variability_analysis(model, reaction_list=None, loopless=None, fraction_of_optimum=1.0, pfba_factor=None, processes=None)
- 基因/反应敲除：src/cobra/flux_analysis/deletion.py → single_gene_deletion(model, gene_list, method="fba")
- 在线取模型：src/cobra/io/web/load.py → cobra.io.load_model(model_id)（BiGG→BioModels 依次搜索，带本地缓存）

可运行示例（Python 3.8+，先 pip install cobra）：

    import cobra
    from cobra.flux_analysis import pfba, flux_variability_analysis, single_gene_deletion

    # 1) 数据获取（首次需联网，之后走缓存）
    model = cobra.io.load_model("iML1515")   # 或 read_sbml_model("iML1515.xml")
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0  # 限制葡萄糖摄取 mmol/gDW/h

    # 2) FBA：最大生长
    sol = model.optimize()   # sol.objective_value / sol.fluxes / sol.shadow_prices
    print(sol.objective_value)

    # 3) pFBA：保持最优生长前提下最小化总通量（酶用量代理，Lewis 2010 MSB）
    psol = pfba(model)

    # 4) FVA：各反应通量可行区间（90% 最优生长下）
    fva = flux_variability_analysis(model, fraction_of_optimum=0.9)  # DataFrame: minimum/maximum

    # 5) 基因必需性扫描 → 靶点优先级
    res = single_gene_deletion(model, model.genes, method="fba")  # DataFrame: growth 列
    essential = res[res["growth"] < 1e-6].index.tolist()  # 必需基因 → 勿做敲除靶点

依赖与安装：pip install cobra（自带 optlang + GLPK 即可跑通；大规模 FVA 建议再装 gurobi/cplex 或 scipy 求解器，速度提升明显）。

### 2.2 WGS 变异解析（breseq，本地 methods/repos/breseq-master）

文档：docs/usage-breseq.md、docs/tutorial-curation-running-breseq.md；测试样例：tests/lambda_mixed_pop/testcmd.sh、tests/REL606_fragment_is_mediated_dels/。核心命令：

    # 安装（推荐 conda；Windows 请用 WSL2）
    conda install -c bioconda breseq

    # 单菌株变异检测：参考基因组 + 双端 reads
    breseq -r NC_000913.3.gbk -o output_betaAla -j 8 -n betaAla_strain sample_R1.fastq.gz sample_R2.fastq.gz

    # 混合群体（传代池、多克隆）加 -p 预测多态性
    breseq -r NC_000913.3.gbk -o output_pool -p -j 8 pool_R1.fastq.gz pool_R2.fastq.gz

    # 结果 → VCF（供下游注释/ML 特征提取）
    gdtools GD2VCF -f output_betaAla/data/reference.fasta -o variants.vcf output_betaAla/output/annotated.gd

输入输出：输入为参考 GenBank/GFF3/FASTA（可多 -r 同时给染色体+质粒）与 FASTQ；输出目录含 output/index.html（可视化报告）、output/annotated.gd（最终变异集）、data/reference.bam、data/reference.fasta。GD 格式变异类型：SNP/SUB/DEL/INS/MOB(转座)/AMP(扩增)/INV/CON/INT。常用 gdtools 子命令：GD2VCF、VCF2GD、FILTER、MASK（屏蔽重复区）、COMPARE。运行时依赖 bowtie2（可选 gnuplot/phylip）；从源码编译需先 ./bootstrap.sh && ./configure && make（仓库 CLAUDE.md 强调，跳过 bootstrap 会报 "No targets"）。

### 2.3 编辑效率分析（CRISPResso2，本地 methods/repos/CRISPResso2-master）

核心源码：CRISPResso2/CRISPRessoCORE.py（比对+indel 定量）、CRISPResso2/CRISPRessoPlot.py（绘图）；参数定义集中在 args.json。输入格式样例见 tests/FANC.batch（batch 表：样本名<TAB>fastq路径）与 tests/Cas9.amplicons.txt（扩增子名<TAB>扩增子序列<TAB>gRNA序列）。

    # 安装：pip install CRISPResso2（Python 3，numpy<2；或 conda -c bioconda crispresso2 / docker）

    # 单扩增子（β-丙氨酸课题：panD/aspC 位点）
    CRISPResso -r1 edited_R1.fastq.gz -a <AMPLICON_SEQ> -g GGAATCCCTTCTGCAGCACC -o CRISPResso_on_panD --min_frequency_alleles_around_cut_to_plot 0.001

    # 批量多样本（对照 vs 编辑，同一 gRNA）
    CRISPRessoBatch -bs batch.txt -a <AMPLICON_SEQ> -g <GUIDE_SEQ> -o CRISPRessoBatch_out

    # 跨样本比较（编辑 vs 未处理对照）
    CRISPRessoCompare CRISPResso_on_Untreated/ CRISPResso_on_Cas9/

关键输出：CRISPResso_quantification_of_editing_frequency.txt（编辑频率定量：unmodified/modified 计数、indel 比例）、Alleles_frequency_table.txt（等位基因谱）、CRISPResso_plot_*（indel 分布图）。指标口径：以 gRNA 切割位点附近（默认 ±3bp，可调）是否含 indel 判定"modified"；编辑效率 = (总 reads - 未修饰 reads)/总 reads。pooled/WGS 模式需额外 bowtie2+samtools。

### 2.4 RNA-seq 差异分析（DESeq2，文献卡 S_Moderated_estimation...）

    # BiocManager::install("DESeq2")；输入：featureCounts/htseq 基因计数矩阵
    library(DESeq2)
    cts <- read.table("counts.tsv", header=TRUE, row.names=1)   # 行=基因，列=样本
    coldata <- data.frame(condition=c("ctrl","ctrl","ctrl","edit","edit","edit"))  # 至少 3 生物学重复！
    dds <- DESeqDataSetFromMatrix(countData=cts, colData=coldata, design=~condition)
    dds <- DESeq(dds)   # 内置离散度+LFC 经验贝叶斯收缩
    res <- results(dds, alpha=0.05)   # 独立过滤 + BH FDR
    resShrunk <- lfcShrink(dds, coef="condition_edit_vs_ctrl", type="apeglm")  # 收缩 LFC
    sig <- subset(as.data.frame(resShrunk), padj < 0.05 & abs(log2FoldChange) >= 1)
    rlogMat <- assay(rlog(dds, blind=TRUE))   # 方差稳定变换 → ML 输入特征

要点（源自文献卡）：默认 median-of-ratios 归一化；离散度按均值-丰度趋势收缩、LFC 向零收缩（报告时应同时给 MLE 与 shrunken 值）；Cook distance 离群点处理要求条件重复≥3；阈值检验 results(..., altHypothesis="greaterAbs", lfcThreshold=1) 可筛"生物学显著"基因。

## 3. 大模型训练代码

本路线的"大模型"任务是编辑效应预测：输入 = gRNA 靶基因/位点特征 + FBA 通量特征 + 表达特征，输出 = 菌株生长/产物滴度（β-丙氨酸或高丝氨酸）。PyTorch 骨架（依赖：torch、pandas、numpy、scikit-learn；特征工程需先跑通第 2 节各管线）：

    import numpy as np, pandas as pd, torch, torch.nn as nn
    from torch.utils.data import TensorDataset, DataLoader
    from sklearn.model_selection import KFold
    from sklearn.preprocessing import StandardScaler

    # 特征组装（伪代码 → 真实 API 混合；按你的数据格式适配）
    # 每行 = 一个 gRNA→基因→菌株实验：X = concat([
    #   gRNA 序列 one-hot/embedding(30nt),
    #   FBA 特征: pFBA 类别(essential/optima/ELE/MLE/no-flux one-hot)、FVA 区间宽度、敲除后生长通量(single_gene_deletion 输出),
    #   DESeq2 rlog 表达向量(靶基因邻域, 可 PCA 降维到 top-K) ])
    # y = 滴度(g/L) 或 相对生长速率

    class TiterNet(nn.Module):
        def __init__(self, d_in, d_hidden=256, dropout=0.3):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(d_in, d_hidden), nn.BatchNorm1d(d_hidden), nn.ReLU(), nn.Dropout(dropout),
                nn.Linear(d_hidden, d_hidden), nn.ReLU(), nn.Dropout(dropout),
                nn.Linear(d_hidden, 1))
        def forward(self, x): return self.net(x).squeeze(-1)

    def train(model, X, y, epochs=300, lr=1e-3, wd=1e-2, bs=32):
        opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs)
        lossf = nn.MSELoss()
        ds = TensorDataset(torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32))
        dl = DataLoader(ds, batch_size=bs, shuffle=True)
        for ep in range(epochs):
            model.train()
            for xb, yb in dl:
                opt.zero_grad(); loss = lossf(model(xb), yb); loss.backward(); opt.step()
            sched.step()   # 验证集早停 patience=20，保存 best.pt（此处省略）
        return model

    # 5 折交叉验证评估：R2 与 Pearson r；样本<100 时改用留一法/嵌套 CV
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    for tr, va in kf.split(X):
        m = train(TiterNet(X.shape[1]), X[tr], y[tr])   # 在 X[va] 上算 MSE/R2

超参数建议（结合文献卡）：DESeq2 差异基因阈值 FDR<5% + |log2FC|>=1 作特征筛选；pFBA 分类与富集检验沿用 Lewis 2010 的超几何 + 10000 次置换 + FDR=0.1；训练用 AdamW(lr=1e-3, wd=1e-2) + CosineAnnealing + 早停；BatchNorm+Dropout(0.3) 防小样本过拟合。注意：若实验样本量不足（<50），不要硬训深度模型——先跑随机森林/XGBoost 基线并做特征重要性分析，把 FBA 特征作为可解释先验注入；生长耦合产物设计用约束建模（OptKnock/MOMA，cobrapy 生态）而非 DL。需查证：rlog 表达矩阵降维维度与 gRNA 嵌入维度需按数据定。

## 4. 解释文档（中文）

- FBA 与 pFBA：FBA 在稳态假设下（dX/dt=0）把代谢网络写成线性约束（S*v=0，S 为化学计量矩阵），最大化目标（如生物量）；解不唯一 → FVA 求每个反应通量可行区间；pFBA 在保持最大生长前提下再最小化总通量绝对值（酶用量代理），把基因分成 essential / pFBA optima / ELE(酶学低效) / MLE(代谢低效) / no-flux 五类——这正是"应增强/应敲低"靶点清单的计算来源。常见坑：①默认培养基上下界不反映真实发酵条件，需按实验设定葡萄糖/氧/氮摄取；②iML1515 求解较慢，FVA 加 processes 并行、大模型换商业求解器；③敲除必需基因直接无解(infeasible)，靶点筛选中必须排除。
- 与 β-丙氨酸/高丝氨酸课题的关联：β-丙氨酸经 L-天冬氨酸-α-脱羧酶(panD 通路，天冬氨酸家族)；高丝氨酸由天冬氨酸半醛经 thrA/hom 等生成。用 iML1515 对通路基因做 pFBA 分类 + FVA 区间，可得到"敲低竞争分支(lysC/metA 分流)、增强目标分支"的计算证据；RegulonDB 的 -400/+100 调控区域约束 gRNA 落点不破坏全局调控（避开 CRP/Cra 等关键 TFBS）。
- breseq：短 reads → bowtie2 双阶段比对 → junction candidate → 变异判定 → HTML/GD 输出；GD 是 tab 分隔文本，可用 gdtools 转 VCF 进 ML 特征。常见坑：重复序列/IS 元件区易误报，用 MASK 屏蔽；混合群体必须加 -p；报告须同时写 breseq 与 bowtie2 版本（结果随版本微变）。
- CRISPResso2：以扩增子为参考做比对，统计切割点附近 indel 判定"修饰/未修饰"，给出编辑效率与等位基因谱。常见坑：扩增子序列必须与引物设计一致（含 gRNA 与切割位点）；numpy<2 的版本约束；批量样本统一用 batch 文件；低覆盖样本用 --min_frequency_alleles_around_cut_to_plot 过滤噪声等位基因。
- DESeq2：负二项 GLM + 经验贝叶斯收缩，专治 3~4 个生物学重复的小样本；rlog 变换后矩阵方差齐性，适合做 ML 输入；Cook distance 自动处理离群样本（需≥3 重复）。常见坑：2 个重复无法做离群点检测；大肠杆菌多顺反子操纵子需按转录单元聚合计数；报告用 shrunken LFC 而非原始 MLE。
- 数据库：EcoCyc 管"基因-反应-通路"注释，RegulonDB 管"TF-TFBS-调控区域"，BiGG 管 GEM 模型；三者以基因名为键可 JOIN 成一张靶点知识表，作为 AI 选靶的特征层与 LLM RAG 语料。

## 5. 行动项

1. 【P0 · 8/25 前】环境与数据落地：装好 cobra/breseq/CRISPResso2/DESeq2 四个环境（Windows 用户 breseq 走 WSL2）；下载 iML1515 SBML、NC_000913.3 gbk、EcoCyc flat files、RegulonDB 下载包到本地，并在 README 记录版本号。
2. 【P0】iML1515 靶点分类脚本：写 routeE_pfba_classify.py，对 panD/aspC 通路及全基因组跑 FBA+pFBA+FVA+必需性，输出"应增强/应敲低/必需勿动"三类基因清单，作为 AI 选靶的约束输入。
3. 【P1 · 9/20 前】编辑验证迷你管线：用 CRISPResso2 对 1 个 gRNA 位点（可先用公开 FANC 测试数据，见 repos/CRISPResso2-master/tests/）跑通 fastq→编辑效率→等位基因谱，再套 breseq 对同一菌株 WGS 确认无意外大变异；两条命令固化进 run_validation.sh。
4. 【P1】多组学一致性报告：把 DESeq2 差异基因（FDR<5%, |log2FC|>=1）与 pFBA 五类基因做超几何富集，输出"模型预测 vs 实测"一致性图（复现 Lewis 2010 思路），作为"AI 设计→实验验证→模型闭环"的证据。
5. 【P2】编辑效应预测模型：按第 3 节骨架组装特征（gRNA 序列 + FBA 特征 + rlog 表达），小样本先跑 RF 基线，提交材料展示特征重要性（FBA 特征是主要贡献）即可。

> 时间线：P0（基线）→ P1（管线打通）→ P2（模型收尾）。所有无法确认的下载链接以"需查证"标注，落地前统一验证。
