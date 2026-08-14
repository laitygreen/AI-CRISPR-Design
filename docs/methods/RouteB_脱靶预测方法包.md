# RouteB 脱靶预测方法学习包

> 路线主题：CRISPR/Cas9 脱靶预测（检测数据 → 特征 → 模型 → 评估）
> 本路线对应项目 M2 脱靶评估模块，服务于大肠杆菌 β-丙氨酸/高丝氨酸细胞工厂的 sgRNA 设计与编辑安全性筛选。

## 0. 路线总览

**解决的问题**：给定一条 sgRNA（20 nt + NGG PAM），预测其在整个基因组上对"非目标位点"（off-target，OTS）的切割活性，从而在候选 sgRNA 中筛出"效率高且脱靶低"的最优设计，避免误伤必需基因、保证菌株稳定性。

**子路线（多途径方法，可组合）**：
1. **检测数据驱动**：用 GUIDE-seq / CIRCLE-seq / SITE-seq / CHANGE-seq / Digenome-seq 等实验检测数据直接获得"位点→活性标签"，作为训练与验证集；大肠杆菌小基因组还可做**简化全基因组重测序（WGS）**直接观察编辑后的突变谱作为黄金验证。
2. **序列特征 + 经典模型**：错配位置、种子区（PAM 近端 ~12 bp）、PAM 类型、bulge（插入/缺失）、GC 含量、局部表观特征；CFD 规则、Elevation、SVM/GBDT/XGBoost 等。
3. **深度学习**：CNN/RNN（CRISPR-Net 的 RCNN、DeepCRISPR 的 8 通道 CNN），输入为 on/off 序列对的对齐编码。
4. **预训练 DNA 语言模型**：DNABERT(-Epi) / DNABERT-2 微调，两阶段（先学错配位置、再学二分类），叠加表观特征多模态融合。

**适用场景**：sgRNA 大规模筛选（先全基因组枚举候选 → 模型打分排序）、低脱靶设计约束、编辑后 WGS 复核。本路线以"分类（活性/非活性）为主、回归（活性读数）为辅"，因为极端不平衡数据下分类更稳健（DeepCRISPR 原文亦证实）。

## 1. 公共数据库与资源原件

| 数据/模型/工具 | 来源 | 获取方式 | 用途 | 注册/授权 |
|---|---|---|---|---|
| CRISPR-Net 全套数据（CIRCLE-seq I-1、GUIDE-seq II-4/5/6、SITE-seq II-3、Elevation II-1/2，含 indel 与纯 mismatch） | JasonLinjc/CRISPR-Net (GitHub) | 本地已下载：methods/repos/CRISPR-Net-master/data/；在线：github.com/JasonLinjc/CRISPR-Net | 脱靶训练/测试集（人源），复现 AUROC/AUPR | 无需 |
| CRISPR-Net 预训练权重（CIRCLE+elevation+SITE 训练） | 同上 | 本地 code/scoring_models/CRISPR_Net_CIRCLE_elevation_SITE_weights.h5 + _structure.json | 直接打分（Keras），或转 PyTorch 复用 | 无需 |
| DeepCRISPR off-target 数据（30 sgRNA、约 16 万候选、约 700 正例，GUIDE-seq/Digenome/BLESS/HTGTS/IDLV 五平台） | bm2-lab/DeepCRISPR | 本地 paper_data-classification.tar.gz；Zenodo 1246320；github.com/bm2-lab/DeepCRISPR | 经典基线的训练/对比数据（1:250 不平衡） | 无需 |
| DeepCRISPR 预训练模型（offtar_pt_cnn / offtar_pt_cnn_reg，TF1 格式） | 同上 | 本地 trained_models/*.tar.gz（先解压） | 8 通道 CNN 基线 | 无需 |
| CHANGE-seq（110 sgRNA，20 万活性 OTS）、GUIDE-seq（Tsai 2015 等）原始数据 | 原始论文补充材料 | 下载链接需查证（文献卡标注"文中未提供直接下载"）；整理版见 dagrate/public_data_crisprCas9 | 大规模训练/外部验证 | 需查证 |
| 整理后基准数据 + one-hot 预处理脚本 | dagrate/public_data_crisprCas9 (GitHub) | github.com/dagrate/public_data_crisprCas9 | 统一去泄漏协议的跨工具对比 | 无需 |
| DNABERT 预训练权重（3/4/5/6-mer，MLM） | zhihan1996/DNABERT | HuggingFace：huggingface.co/zhihan1996/DNA_bert_3（README 2025-07-08 更新，原 Google Drive 链接已失效） | 脱靶微调底座（DNABERT-Epi 用 3-mer） | 无需 |
| DNABERT-Epi 复现代码（含 5 个基线重实现） | kimatakai/CRISPR_DNABERT | github.com/kimatakai/CRISPR_DNABERT（文献卡提供，链接需查证） | 两阶段微调 + 表观融合参考实现 | 需查证 |
| 表观特征数据（H3K4me3/ATAC-seq/H3K27ac，人源） | GEO | GEO 号 GSE149363 | DNABERT-Epi 表观通道（E. coli 需替换为原核特征） | 公开 |
| ENCODE 表观数据（CTCF/DNase/H3K4me3/RRBS） | ENCODE | encodeproject.org | DeepCRISPR 8 通道特征 | 公开 |
| E. coli K-12 MG1655 参考基因组 | NCBI | GCF_000005845.2（genbank/ncbi 下载） | 全基因组脱靶候选枚举与 WGS 比对 | 无需 |
| 在线工具：CRISPOR、Cas-OFFinder | 官网/GitHub | crispor.tefor.net；github.com/snugel/cas-offinder | 候选位点枚举（≤3 错配）与交叉验证 | 无需 |
| EcoCyc / RegulonDB | 数据库官网 | ecocyc.org；regulondb.ccg.unam.mx | E. coli 基因必需性、操纵子/表达特征 | 注册（学术免费） |

## 2. 生信处理代码参考（本地仓库实测路径）

### 2.1 CRISPR-Net（RCNN，支持 indel 与 mismatch）
- **编码**：methods/repos/CRISPR-Net-master/code/Encoder_sgRNA_off.py 中 Encoder(on_seq, off_seq) 类，把 on/off 序列对齐为固定 24 位，输出 **24×7 通道**编码（5-bit 字符通道 A/T/G/C/_/N + 2-bit 方向通道，显式编码错配/插入/缺失，无信息损失）。数据加载函数在 code/encode_data.py：load_CIRCLE_data()、load_elevation_guideseq_data()、load_siteseq_data()、load_Kleinstiver_data() 等，输入 CSV 列 sgRNA_seq/off_seq/label(或Read)。
- **模型定义与重训**：code/evaluate_CRISPR_Net.py 中 CRISPR_Net_model()：多尺度 Conv2D（kernel (1,1)/(1,2)/(1,3)/(1,5)）→ Concatenate → Reshape(24,47) → BiLSTM(15) → Dense(80/20) → Dropout(0.35) → Sigmoid。
- **直接打分命令**（依赖 Python3.6 + Keras 2.2.4 + TF1.12，需适配）：
```bash
cd "exp design/methods/repos/CRISPR-Net-master/code"
# 输入两列: on_seq,off_seq（"_"表示indel），输出 results/CRISPR_net_results.csv 的 CRISPR_Net_score
python CRISPR_Net.py input_examples/on_off_seq_pairs.txt
# 聚合单条 gRNA 的整体脱靶分数（多 OTS 汇总）
python CRISPR_Net_Aggregate.py input_examples/aggregate_example_GACCTTGCATTGTACCCGAG.csv
```
- **环境**：environment/Dockerfile（Code Ocean 胶囊）可重建；本机建议 conda 建 py3.6 环境或直接转写为 PyTorch（见 §3）。

### 2.2 DeepCRISPR（统一框架，8 通道 + 表观）
- 编码：核苷酸 4 通道 + CTCF/DNase/H3K4me3/RRBS 4 个表观通道 = **8 通道 × 23 位**"类图像"输入；数据格式见 examples/*.epiotrt（off-target：Id, on 序列, on 表观×4, off 序列, off 表观×4, Label，表观用 A/N 表示有/无信号）。
- 推理示例（run_examples.py）：
```python
import tensorflow as tf, deepcrispr as dc
from deepcrispr import DCModelOfftar
sess = tf.InteractiveSession()
dcm = DCModelOfftar(sess, 'trained_models/offtar_pt_cnn', is_reg=False)   # 或 offtar_pt_cnn_reg
pred = dcm.offtar_predict(x_on, x_off)   # 各 [batch, 8, 1, 23]
```
- 依赖：python3.6 + tensorflow 1.3.0 + sonnet 1.9（同样需适配/仅作基线参照）。

### 2.3 DNABERT（微调底座）
- 数据格式：examples/sample_data/ft/6/train.tsv（sentence\tlabel，sentence 为 k-mer 化序列）；转 k-mer 用 examples/data_process_template/process_finetune_data.py 的 get_kmer_sentence(seq, kmer) 或 motif/motif_utils.py 的 seq2kmer。
- 微调命令（examples/run_finetune.py，transformers 二分类）：
```bash
cd "exp design/methods/repos/DNABERT-master/examples"
export KMER=3 MODEL_PATH=<预训练权重目录> DATA_PATH=<tsv目录> OUTPUT_PATH=./ft/3
python run_finetune.py --model_type dna --tokenizer_name dna$KMER \
  --model_name_or_path $MODEL_PATH --task_name dnaprom --do_train --do_eval \
  --data_dir $DATA_PATH --max_seq_length 100 \
  --per_gpu_train_batch_size 32 --learning_rate 2e-4 --num_train_epochs 5.0 \
  --output_dir $OUTPUT_PATH --evaluate_during_training
```
- 注意：DNABERT 序列长度限制约 512 token（3-mer 下约 1500 bp 窗口），脱靶输入远小于此，直接拼接即可。

### 2.4 简化 WGS 验证（可选，大肠杆菌）
- 本地 methods/repos/breseq-master（breseq，细菌突变检测）：对编辑前后菌株 WGS fastq 比对 MG1655 参考，输出突变表（breseq -r GCF_000005845.2.fna sample_R1.fastq sample_R2.fastq -o out/），用变异座位与模型预测的高风险 OTS 做重叠率验证。

## 3. 大模型训练代码（PyTorch 骨架，可运行思路）

### 3.1 数据预处理（真实函数名 + 需适配标注）
```python
# 依赖: pandas numpy biopython sklearn; 输入: CRISPR-Net 格式 CSV(sgRNA_seq,off_seq,label)
def build_dataset(csv_path):
    df = pd.read_csv(csv_path)
    X_code, y = [], []
    for _, r in df.iterrows():
        on, off = r['sgRNA_seq'].upper(), r['off_seq'].upper()
        # 方案A: 24x7 编码（适配自 Encoder_sgRNA_off.Encoder，含 indel 占位符）
        X_code.append(encode_dim7(on, off))          # [24,7]
        # 方案B(DNABERT): 3-mer 化后拼 [CLS]on[SEP]off[SEP]（用 seq2kmer）
    return torch.tensor(np.array(X_code)), torch.tensor(y)
# 不平衡处理: 负类随机降采样至 20%（固定种子），正类保留——DNABERT-Epi 文献卡方案
# 划分: GroupKFold(n_splits=10) 按 sgRNA 分组（同 sgRNA 位点必须同折，防泄漏）
```

### 3.2 模型定义
```python
class CRISPR_Net_PyTorch(nn.Module):        # 复刻 evaluate_CRISPR_Net.py 的 RCNN
    def __init__(self, in_ch=7, L=24):
        super().__init__()
        self.branches = nn.ModuleList([nn.Conv2d(1,10,(1,k),padding=(0,k//2)) for k in (1,2,3,5)])
        self.lstm = nn.LSTM(47, 15, bidirectional=True, batch_first=True)
        self.head = nn.Sequential(nn.Linear(24*30,80), nn.ReLU(), nn.Linear(80,20),
                                  nn.ReLU(), nn.Dropout(0.35), nn.Linear(20,1))
    def forward(self, x):                   # x: [B,1,24,7]
        x = torch.cat([b(x) for b in self.branches]+[x], dim=1)
        x = x.permute(0,2,3,1).reshape(-1,24,47)
        x,_ = self.lstm(x); x = x.reshape(x.size(0),-1)
        return self.head(x).squeeze(-1)
# DNABERT 微调（transformers）: BertForSequenceClassification + DNATokenizer.from_pretrained('zhihan1996/DNA_bert_3')
# 输入 = tokenizer 拼接 on/off 序列; loss = CrossEntropy; 训练参数参考 DNABERT-Epi 卡:
#   阶段一(错配位置预测) batch 8, lr 2e-5, 5 epochs; 阶段二(二分类) batch 256, lr 2e-5, 5 epochs
```

### 3.3 训练循环与评估
```python
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score, matthews_corrcoef
gkf = GroupKFold(n_splits=10)
for tr, te in gkf.split(X, y, groups=sgRNA_ids):     # 按 sgRNA 分组
    model.fit(X[tr], y[tr], epochs=5, batch_size=256, lr=2e-5)   # AdamW
    p = torch.sigmoid(model(X[te])).numpy()
    print(roc_auc_score(y[te], p), average_precision_score(y[te], p),
          f1_score(y[te], p>0.5), matthews_corrcoef(y[te], p>0.5))
# 5 个随机种子重复 → 均值±标准差 + Wilcoxon 检验（对比基线）——文献卡标准协议
```
- **超参数建议**（源自文献卡/原仓库）：CRISPR-Net：多尺度核 (1,1/2/3/5)、BiLSTM 15 单元、Dropout 0.35；DNABERT-Epi：两阶段 lr 2e-5、5 epochs、EPI 融合 FNN(32)+dropout(0.1)（对 E. coli 把 H3K4me3/ATAC 换成 RNA-seq 表达/GC/操纵子等原核特征，标注为需适配）；不平衡：负采样 20% 或 mini-batch 1:1 bootstrapping（DeepCRISPR 方案）。
- **依赖**：python≥3.9、torch≥2.0、transformers≥4.40、scikit-learn、pandas；DNABERT 3-mer 权重从 HuggingFace 拉取（国内网络需镜像/代理，需查证）。

## 4. 解释文档（中文）

**检测技术原理**：GUIDE-seq 用双链寡核苷酸（dsODN）标签整合到双链断裂处再测序，检测细胞内真实脱靶；CIRCLE-seq 将基因组环化后体外线性化，灵敏度最高但为体外环境；SITE-seq/Digenome-seq 依赖核酸酶切割后测序峰；CHANGE-seq 为高灵敏度体外法（110 sgRNA 级别的大规模数据）；**简化 WGS** 直接对编辑菌株全基因组重测序，用 breseq 找变异，是最接近"真实后果"的验证，成本低但灵敏度受测序深度限制。

**核心特征**：①**错配位置**：PAM 远端（5' 端）错配容忍度高、近端（seed 区，PAM 前 1~12 bp）错配高度敏感；②**种子区**（seed region）：决定 R-loop 形成，是错配惩罚加权的重点；③**PAM 类型**（NGG>NAG 等）；④**bulge**（插入/缺失导致的对齐空隙，CRISPR-Net 专门支持）；⑤**表观特征**（人源染色质开放性/组蛋白修饰；原核无染色质域，改用表达水平、复制方向、GC 等）。

**模型谱系**：CFD 规则（Hsu 2013，位置×碱基错配加权表，可作最简基线）；Elevation（Listgarten 2018，位置独立模型，AUROC≈0.98）；CRISPR-Net（RCNN，AUROC 0.995/AUPR 0.317）；DeepCRISPR（预训练+8 通道 CNN，AUROC 0.981/PR-AUC 0.497）；DNABERT-Epi（两阶段微调 + 表观融合，GUIDE-seq 上 PR-AUC 显著最优，集成后全面最优）。

**不平衡处理**：off-target 正负比极端（1:250 ~ 1:1394），直接训练会退化为"全预测负类"；常用：负类随机降采样（如 20%）、mini-batch 内 1:1 bootstrapping、focal loss。

**评估**：**AUROC** 对类别不平衡不敏感、适合整体排序能力；**AUPR（PR-AUC）** 聚焦少数正类、更贴近"在低假阳性下找真脱靶"的决策需求，务必两个都报；补充 F1/MCC（阈值相关）。

**常见坑**：①数据泄漏——同 sgRNA 的位点必须同折分组（GroupKFold），否则指标虚高；②方向/补丁——on/off 序列需统一 5'→3' 对齐，indel 用占位符编码；③旧代码适配——CRISPR-Net（Keras/TF1）、DeepCRISPR（TF1+sonnet）与 CUDA 12 冲突，建议只移植编码与架构、用 PyTorch 重训；④DNABERT 预训练权重旧链接已失效，一律从 HuggingFace 获取；⑤**人源模型不能直接用于大肠杆菌**——基因组仅 4.6 Mb、无染色质域、密码子/GC 组成不同，必须用 E. coli 参考基因组重枚举候选并微调。

**与 β-丙氨酸/高丝氨酸课题的关联**：设计敲除（如 β-丙氨酸途径竞争节点 aspC/aspA 或高丝氨酸途径 thrA 操纵子相关基因）或整合表达盒的 sgRNA 时，脱靶模型用于：①在候选 sgRNA 中筛掉会误伤必需基因（对照 EcoCyc 必需基因表）的序列；②对最终选定的 2~3 条 sgRNA 做 WGS 复核，把"脱靶数"作为菌株安全性指标写入提交材料。

## 5. 行动项（可直接落地，按优先级）

1. **[P0] 复现脱靶基线并统一评估**：在本地 CRISPR-Net/DeepCRISPR 数据上，用 §3 的 PyTorch 骨架重训 CNN 基线，按 sgRNA 分组 10 折 CV，报告 AUROC/AUPR/F1/MCC（1 周内）。责任人：模型组。
2. **[P0] 构建 E. coli 脱靶数据集**：下载 MG1655 参考基因组（GCF_000005845.2），用 Cas-OFFinder 枚举 ≤3 错配候选；正例来源：文献报道的 E. coli 编辑位点 + 可选简化 WGS 自测；负例随机采样，正负比设 1:50~1:100（1~2 周）。
3. **[P1] 训练 CNN 基线 + 不平衡处理**：24×7 编码（适配自 CRISPR-Net Encoder），负采样 20% + mini-batch 1:1，验证集按 sgRNA 分组，与 CFD/Elevation 规则对比（1 周）。
4. **[P1] 微调 DNABERT 3-mer 两阶段模型**：错配位置预测 → 脱靶二分类；E. coli 特征通道（RNA-seq 表达/GC/复制方向）替代人源表观；与 CNN 基线对比（2 周）。
5. **[P2] 集成 + 可解释输出**：软投票集成（CNN+DNABERT+LightGBM），注意力/SHAP 归因输出"脱靶风险主要来自哪些位置"，接入最终 sgRNA 排序与报告模块；为提交材料生成 E. coli 脱靶谱可视化（3 周）。

---

*未确认项均标注"需查证"（CHANGE-seq/GUIDE-seq 原始数据直链、kimatakai/CRISPR_DNABERT 仓库可用性、HuggingFace 国内网络访问）。引用文献卡：DNABERT-Epi（bioRxiv 2025 预印本）、DeepCRISPR（Genome Biol 2018）、CRISPR-Net（Bioinformatics 2021，本地源码）、ML/DL 综述（Brief Bioinform 2023）。*
