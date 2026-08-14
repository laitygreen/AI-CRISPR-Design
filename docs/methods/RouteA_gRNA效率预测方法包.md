# RouteA gRNA 编辑效率预测 方法学习包

> 适用：赛道二"AI 基因编辑"（9/5 报名，10/4 提交）；本包对应 M1（gRNA 效率预测）+ B2（统一评测）模块，为大肠杆菌（E. coli MG1655）β-丙氨酸 / L-高丝氨酸细胞工厂的基因敲除 sgRNA 设计提供模型底座。

## 0. 路线总览

- **解决什么问题**：给定 20 nt spacer + PAM 上下文，预测 sgRNA 的**编辑效率**（回归：敲除效率/indel 频率；分类：高低效率二值）。这是 CRISPR 基因编辑设计的"第一关"——先选出高效 sgRNA，再谈脱靶（RouteB）与代谢通路改造（M3）。
- **两条子路线**：
  - **A-1 旧版 TF1 复现（经典基线）**：复现 DeepCRISPR（TensorFlow 1.3 + Sonnet，2018）与 Azimuth（Doench 2016，sklearn 时代），用于对照和"复古基线"卖点，环境用 Docker 隔离。
  - **A-2 现代 PyTorch 重实现（主攻）**：按 CRISPRon（Nat Commun 2021）的"多尺度 CNN + ΔGB 热力学特征"架构，用 PyTorch 重写训练/推理，并预留 Transformer 编码器替换口（参考 AttCRISPR、TransCrispr）。
- **适用场景**：人源数据训练→迁移受限，最终需用 E. coli 自身数据重训（综述明确"物种特异模型是硬需求"，Wang & Zhang 2019 的 E. coli CNN 为佐证）；本包先跑通人源公开数据管线，再把数据源换成 E. coli。
- **决策树**：快速验证 → 用 A-1/Azimuth 预训练模型直接打分；要"可训练、可迁移" → A-2 PyTorch CNN+ΔGB；要"可解释+长上下文" → A-2 的 Transformer 变体。三档能力逐级递进，共享同一套 30mer 特征编码与评测协议。
- **备赛定位**：本路线产出三个可交付物——① 复现报告（TF1 旧框架 vs PyTorch 新实现的性能/耗时对比，本身就是答辩加分项）；② E. coli 专属 gRNA 效率模型与打分脚本；③ 一套防泄漏的评测基准，用于回答"你的模型比已有工具强在哪"。

## 1. 公共数据库与资源原件

| 数据/模型/工具 | 来源 | 获取方式（本地/链接） | 用途 | 注册/授权 |
|---|---|---|---|---|
| CRISPRon 代码+6 个预训练模型 | RTH-tools/crispron | 本地 `methods/repos/crispron-main`；GitHub: https://github.com/RTH-tools/crispron | A-2 主架构参考+直接推理 | 开源 AGPL-3，无需注册 |
| CRISPRon 23,902 条 gRNA 训练数据 | CRISPRon 官网 | https://rth.dk/resources/crispr/crispron/download（**需查证**是否需邮箱申请）；GEO: GSE173708 | 训练/外部验证集 | 需查证 |
| CRISPRoff 能量模型（ΔGB） | RTH.dk | https://rth.dk/resources/crispr/crisproff/download → 拷贝 `CRISPRspec_CRISPRoff_pipeline.py` 到 crispron/bin、`energy_dics.pkl` 到 data/model/ | 热力学特征计算 | 需查证 |
| DeepCRISPR 代码+预训练模型 | bm2-lab/DeepCRISPR | 本地 `methods/repos/DeepCRISPR-master`（`trained_models/*.tar.gz` 需先解压）；Zenodo: https://zenodo.org/record/1246320 | A-1 基线复现 | Apache-2.0，无需注册 |
| DeepCRISPR 训练数据（~1.5 万标注 + 6.8 亿预训练） | DeepCRISPR 论文附件 | 本地 `paper_data-classification.tar.gz`、`paper_data-regression.tar.gz`；http://www.deepcrispr.net/（预训练数据**需查证**） | A-1 复现 | 需查证 |
| Azimuth 代码+数据+V3 模型 | MicrosoftResearch/Azimuth | 本地 `methods/repos/Azimuth-master`（`azimuth/data/V1_data.xlsx`、`V2_data.xlsx`、`saved_models/V3_model_full.pickle`）；`pip install azimuth` | A-1 基线 + Doench 2016 数据集 | MIT，无需注册 |
| 整理好的公开基准集 | dagrate/public_data_crisprCas9 | https://github.com/dagrate/public_data_crisprCas9 | 统一外部评测集 | 开源 |
| E. coli MG1655 参考基因组 | NCBI | NC_000913.3 (U00096.3)；EcoCyc/RegulonDB 注释 | E. coli 30mer 提取、预训练语料 | 无需注册 |
| Doench 2016 (V1/V2) 数据 | Azimuth 仓库内 | 本地 `Azimuth-master/azimuth/data/V1_data.xlsx`、`V2_data.xlsx`、`FC_plus_RES_withPredictions.csv` | A-1 训练/外部验证（2549 条 gRNA、8 基因、A375 细胞） | 开源 |
| E. coli sgRNA 活性数据 | Wang & Zhang 2019 等 | 论文补充材料（**需查证**链接）；CRISPOR 数据库聚合 | E. coli 重训标注 | 需查证 |
| CRISPOR / GenomeCRISPR | CRISPOR 官网 | https://crispor.tefor.net/（聚合 22 个人源数据集、>55 万 sgRNA） | 备选大规模预训练语料 | 免费 webserver |
| ViennaRNA/RNAfold | ViennaRNA | conda 安装（`crispron-main/environment.yml` 已列 viennarna 2.6.4） | spacer 折叠自由能 | 开源 |

## 2. 生信处理代码参考（本地仓库真实路径）

**CRISPRon 推理管线（3 步，A-2 直接可用）**：

```bash
# 环境：conda env create -f methods/repos/crispron-main/environment.yml
cd "methods/repos/crispron-main"
# ① 从 FASTA 提取 30mer（4 nt 上游+20 spacer+3 PAM+3 下游）与 23mer
python3 bin/get_30mers_from_fa.py -f test/seq.fa -m out/30mers.fa -g out/23mers.fa
# ② 计算热力学特征（需 CRISPRoff：CRISPRspec_CRISPRoff_pipeline.py + energy_dics.pkl）
python3 bin/CRISPRspec_CRISPRoff_pipeline.py --guides out/23mers.fa   --specificity_report out/CRISPRspec.tsv --guide_params_out out/CRISPRparams.tsv   --duplex_energy_params data/model/energy_dics.pkl --no_azimuth
# ③ 用 6 个预训练模型平均推理（输出 out/crispron.csv: ID,30mer,CRISPRon 分数）
python3 bin/DeepCRISPRon_eval.py out out/30mers.fa out/CRISPRparams.tsv data/deep_models/best/*/
# 一键版：bash bin/CRISPRon.sh test/seq.fa test/outdir；自检：bash bin/test.sh（期望 TEST ok）
```

关键 API 说明：`DeepCRISPRon_eval.py` 输入为"30mer FASTA + CRISPRparams.tsv（第 7 列为 ΔGB）"，输出取 6 模型预测均值；`get_30mers_from_fa.py` 内置 NGG PAM 扫描（`PAM='GG'`、正负链）。

**DeepCRISPR 推理（A-1 基线）**：

```python
# 需 docker 环境（python3.6 + tensorflow1.3 + sonnet1.9）：
# docker pull michaelchuai/deepcrispr:latest（程序在 /root/DeepCRISPR）
import deepcrispr as dc, numpy as np, tensorflow as tf
data = dc.Sgt('examples/eg_reg_on_target_seq.rsgt', with_y=True)   # 纯序列回归
x, y = data.get_dataset(); x = np.expand_dims(x, axis=2)           # [N,4,1,23]
sess = tf.InteractiveSession()
m = dc.DCModelOntar(sess, 'trained_models/ontar_cnn_reg_seq', is_reg=True, seq_feature_only=True)
pred = m.ontar_predict(x)                                          # 输出效率分数
# 分类/全特征：dc.Episgt(..., num_epi_features=4)；脱靶：dc.Epiotrt + dc.DCModelOfftar
```

编码类 `Sgt/Episgt/Epiotrt` 定义在 `deepcrispr/utils.py`（one-hot：A=(1,0,0,0)…；表观特征 A=1/N=0）。特征编码为"多通道类图像"：4 通道序列 + 每项表观特征 1 通道 = 8 通道 [N,8,1,23]。

DeepCRISPR 模型文件对照（`trained_models/`，先解压再加载）：`ontar_ptaug_cnn`＝预训练+增强分类、`ontar_pt_cnn_reg`＝预训练回归、`ontar_cnn_reg_seq`＝纯序列回归；off-target 用 `offtar_pt_cnn(_reg)`。

**输入格式备忘（DeepCRISPR 示例文件，见 `examples/`）**：on-target 表头 `Chrom|Start|End|Strand|Target Seq|CTCF|Dnase|H3K4me3|RRBS|Label`（Target Seq 为 23 nt＝20 spacer＋3 nt PAM；表观列 A=1/N=0）；off-target 为 `Id|Target Seq|…|Off-target Seq|…|Label`。A-2 管线统一用 CRISPRon 的 30mer 格式，避免格式混用。

**A-2 预处理要点（PyTorch 侧，替换 CRISPRon 的 Keras 读入）**：读取 tsv（列名 `30mer_gRNA`/`Quant_norm_efficiency`/`CRISPRoff`）→ 逐字符 one-hot（A/C/G/T→0/1/2/3）→ ΔGB 数值列转 float32 → 按 Hamming≤8 聚类分 6 折 → 存 `train.pt/val.pt`。

**Azimuth（A-1 轻量基线，pip 即用）**：

```python
import azimuth.model_comparison, numpy as np
seqs = np.array(['ACAGCTGATCTCCAGATATGACCATGGGTT'])
pred = azimuth.model_comparison.predict(seqs, None, None)[0]   # 不含基因位置模型
# 特征参考：azimuth/features/featurization.py —— 30mer 的 1~6-mer 谱特征 + GC + NGGX + Tm + microhomology
```

## 3. 大模型训练代码（A-2 主攻：PyTorch 重实现）

**3.1 数据预处理（对齐 CRISPRon 论文）**：30mer one-hot [N,30,4]；ΔGB 归一化后做第二输入；标签用 Quant_norm_efficiency（rank 归一化）；**去泄漏划分**：按 30mer 两两 Hamming 距离 ≤8 聚类分区（6 折），测试集剔除与对比模型训练集 Hamming ≤6 的 gRNA。

```python
import numpy as np, pandas as pd, torch
def onehot30(seq):                       # seq: 30nt 字符串 → [30,4]
    m = {'A':0,'C':1,'G':2,'T':3}; x = np.zeros((30,4), np.float32)
    for i,c in enumerate(seq.upper()): x[i, m[c]] = 1.0
    return x
df = pd.read_csv('train.csv', sep='\t') # 列: 30mer_gRNA | Quant_norm_efficiency | CRISPRoff(ΔGB)
X = np.stack(df['30mer_gRNA'].map(onehot30).values)          # [N,30,4]
G = df['CRISPRoff'].values.astype(np.float32).reshape(-1,1)  # [N,1]
Y = df['Quant_norm_efficiency'].values.astype(np.float32)    # [N]
# 划分：先按 Hamming 距离≤8 聚类到 6 个 partition，再取 5 份训练 + 1 份验证/测试
```

**3.2 模型骨架（PyTorch，标注适配点）**：

```python
import torch, torch.nn as nn
class CRISPRonNet(nn.Module):   # 复刻 crispron-main/bin/DeepCRISPRon_train.py 结构
    def __init__(self, use_gb=True):
        super().__init__()
        self.br = nn.ModuleList([
            nn.Sequential(nn.Conv1d(4,100,3,padding=1), nn.ReLU(), nn.Dropout(0.3), nn.AvgPool1d(2)),  # k=3
            nn.Sequential(nn.Conv1d(4,70,5,padding=2),  nn.ReLU(), nn.Dropout(0.3), nn.AvgPool1d(2)),  # k=5
            nn.Sequential(nn.Conv1d(4,40,7,padding=3),  nn.ReLU(), nn.Dropout(0.3), nn.AvgPool1d(2)),  # k=7
        ])
        # 30nt→AvgPool→15 位：100*15+70*15+40*15=3150（按 Keras 实现核对维度，可加 Flatten 后 Linear）
        self.fc0 = nn.Sequential(nn.Linear(3150,80), nn.ReLU(), nn.Dropout(0.3))
        self.gb_in = 80 + (1 if use_gb else 0)
        self.fc1 = nn.Sequential(nn.Linear(self.gb_in,80), nn.ReLU(), nn.Dropout(0.3))
        self.fc2 = nn.Sequential(nn.Linear(80,60), nn.ReLU(), nn.Dropout(0.3))
        self.out = nn.Linear(60,1)                       # 回归头（分类任务换 nn.Linear(60,2)+CE）
    def forward(self, x, gb=None):
        h = torch.cat([b(x).flatten(1) for b in self.br], 1)
        h = self.fc0(h)
        if gb is not None: h = torch.cat([h, gb], 1)     # ΔGB 在首个 FC 之后拼接（论文最佳）
        return self.out(self.fc2(self.fc1(h)))
# Transformer 变体（可选）：把三个卷积支路替换为 nn.TransformerEncoder(30, d_model=64, nhead=4)，
# 位置编码用正弦或可学习；参考 AttCRISPR/TransCrispr，需在 E. coli 数据上重调。
```

**3.3 训练循环与超参（引自 CRISPRon 论文/脚本）**：

```python
# 优化器 Adam, lr=1e-4（网格筛过 1e-3/5e-4/1e-4/5e-5）；loss=MSE（回归）/BCE（分类）
# batch=500；EarlyStopping(monitor='val_loss', patience=150)；ModelCheckpoint 存 best
# 6 折 × 每折 5 次随机重复取最优 → 最终 6 个模型预测取平均（DeepCRISPRon_train.py 命令行参数：
# python3 bin/DeepCRISPRon_train.py adam 0.0001 3000 30mer_gRNA Quant_norm_efficiency CRISPRoff 6 6 500 0 CG validation_set*)
```

**3.4 评估指标与代码**：回归用 **Spearman（主，排序一致性）**、Pearson、MSE/MAE；分类用 **ROC-AUC / PR-AUC**（DeepCRISPR 另报 PR-AUC，因正样本稀疏）。

```python
from scipy.stats import spearmanr, pearsonr
from sklearn.metrics import roc_auc_score, average_precision_score
sp = spearmanr(y_true, y_pred).correlation          # 排序一致性（主指标）
pe = pearsonr(y_true, y_pred)[0]                    # 线性相关
auc = roc_auc_score((y_true > thresh).astype(int), y_pred)   # 二值化阈值自定
ap  = average_precision_score((y_true > thresh).astype(int), y_pred)
```

文献参考值（仅作量级参考，须在统一协议下重测）：CRISPRon 内测 Spearman 0.80、外测 ~0.46–0.68；DeepCRISPR on-target 分类 AUC 0.857（预训练+增强）；Azimuth ~0.56（CRISPRon 论文测得）。**指标横向对比必须用同一去泄漏划分**（综述强调"数值直接比较不可行"）；小数据下 LightGBM/XGBoost 基线常反超深度模型，务必先跑简单基线。

## 4. 解释文档（中文）

**方法原理**：① **one-hot 30mer**——把 4 nt 上游+20 nt spacer+3 nt PAM+3 nt 下游编码为 [30,4] 矩阵，CNN 用 3/5/7 三种核宽捕捉位置局部基序（PAM 近端、种子区 8–12 nt）；② **热力学特征**——ΔGB（gRNA-DNA 杂交能-解链能+RNA 折叠惩罚，CRISPRoff 计算）是 SHAP 第一重要特征，其次 GC 含量与 spacer 折叠自由能；③ **多尺度 CNN** 并行卷积→池化→拼接→全连接，ΔGB 在首个全连接后接入（比直拼降 MSE）。DeepCRISPR 的旧范式则是"无监督自编码预训练（6.8 亿 sgRNA）+ CNN 微调 + 5' 端 2 错配数据增强 + mini-batch 1:1 平衡采样"。

**关键概念**：PAM（NGG）决定可编辑位点；种子区（spacer 3' 端 8–12 nt）错配最敏感；多聚 U 终止 U6 转录（PAM 近端回避 T）；跨数据集融合需线性 rescale 对齐尺度（CRISPRon 用 49 对重叠 30mer 拟合，且先验证数据集间 Spearman>0.7 才融合）。

**编码方案选择**：朴素 4×23 one-hot 对 mismatch/indel 信息有损；支持错配/插入缺失显式通道的 7×23、8×23 编码（综述）在脱靶任务更强；A-2 主攻 on-target 时用 30mer one-hot 即可，做 off-target（RouteB）再升级编码。

**训练协议经验值**：早停 patience 150（CRISPRon）或 100（论文消融）；6 折×每折 5 次重复取最优再平均，可显著降低方差；DeepCRISPR 的"预训练+增强+平衡采样"三件套在标注稀疏时收益最大（0.796→0.857 AUC），E. coli 场景建议照搬。

**评估场景设计（借鉴 DeepCRISPR 论文）**：① 独立 20% 测试（随机但防泄漏）；② leave-one-cell-type-out / leave-one-dataset-out（检验泛化，最接近我们"人源→E. coli"的迁移诉求）；③ 与重训的对比工具在相同划分下 apple-to-apple 比较。报告指标时同时给出 Spearman 与 AUROC，避免"只报对自己有利的指标"。

**数据增强与不平衡**：on-target 可在 5' 端前 2 位引入 2 个错配（不影响活性、标签不变）扩充标注；off-target 正负比可达 1:250，须在 mini-batch 内 1:1 平衡采样或负类下采样。

**常见坑**：① 数据泄漏——相似 gRNA 必须聚类分区；② 尺度不统一——多实验效率值需 rank/Quantile 归一化；③ TF1 旧代码与 python3.10/sklearn 新版本不兼容，务必用 Docker/conda 旧环境；④ CRISPRon 预训练模型是 TF2 SavedModel，PyTorch 重实现不能直接加载权重，需重新训练（但 6 个 best 模型可用于人源数据直接打分）。

**与课题关联**：E. coli 无染色质/甲基化，DeepCRISPR 的表观通道要替换为可获取特征（RNA-seq 表达、操纵子内位置、GC、复制方向）；E. coli 基因组 ~4.6 Mb，全 NGG 位点约数十万条，天然适合"预训练+微调"；对 β-丙氨酸（aspC/alaD 通路）与 L-高丝氨酸（thrA 等）敲除基因，用本模型批量筛选 sgRNA 后接脱靶过滤（RouteB）即完成"设计→筛选"闭环。

## 5. 行动项（按优先级）

1. **[P0] 环境与推理打通（1–2 天）**：conda 建 crispron 环境→`bin/test.sh` 自检→用 6 个预训练模型对 test/seq.fa 出 crispron.csv；同时 docker 拉 DeepCRISPR 镜像跑通 on-target 回归。产出：两份"能出分数"的基线脚本。
2. **[P0] PyTorch 骨架跑通（2–3 天）**：下载 CRISPRon 23,902 条数据（需查证获取方式），实现第 3 节模型+Hamming 分区+6 折训练，复现 Spearman≈0.80 量级；同时登记 Doench V2/Azimuth 数据为外部验证集。
3. **[P1] E. coli 训练集构建（3–5 天）**：MG1655 基因组提取全部 NGG 30mer；整合文献 E. coli sgRNA 数据（Wang & Zhang 2019 等）+ 自建 surrogate 载体高通量活性数据（CRISPRon 思路），做线性 rescale 融合；重训 A-2 模型。
4. **[P1] 统一评测协议（穿插）**：固定 LightGBM/SVM 简单基线 + Spearman/Pearson/AUROC 三指标 + 去泄漏划分，形成 B2 评估规范，支撑备赛报告中"相对提升"的可信度。
5. **[P2] 可解释性与交付**：SHAP/显著性图输出设计规则（PAM 近端偏好等），对接 LLM 解释模块与 gRNA 设计推荐界面（rth.dk webserver 形态可参考）。
