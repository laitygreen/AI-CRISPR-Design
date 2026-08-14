# RouteC DNA 预训练模型方法包

> 项目：AI-CRISPR 驱动大肠杆菌氨基酸细胞工厂智能设计
> 时间线：按项目里程碑推进；本路线聚焦"DNA 预训练基础模型（Foundation Model）"的选型、嵌入提取与下游微调。
> 本地代码：`exp design\methods\repos\{DNABERT-master, DNABERT_2-main, nucleotide-transformer-main, hyena-dna-main}`；文献卡：`exp design\knowledge_base\literature\`。

## 0. 路线总览

**解决什么问题**：CRISPR gRNA 设计（效率预测、脱靶评估）和细胞工厂元件设计（启动子/终止子强度、代谢通路基因表达预测）都需要把"DNA 序列"转成机器可用的向量表示。DNA 预训练模型（DNABERT、NT、HyenaDNA 等）用大规模基因组做 MLM/next-token 预训练，学到的嵌入可直接用作下游任务特征或微调底座，避免小数据下从零训练深度模型（文献消融显示随机初始化模型在脱靶任务上 ROC-AUC 仅 0.52，预训练几乎不可替代）。

**子路线（多途径）**：
- **R0 选型基准**：5 模型（DNABERT-2、NT-v2、HyenaDNA、Caduceus-Ph、GROVER）× 3 池化（CLS/mean/max）在大肠杆菌任务上的横向对比（复现 Nature Commun. 2025 基准框架）。
- **R1 冻结嵌入 + 浅层头**：零样本嵌入 + 随机森林/逻辑回归，成本最低、无微调偏置，适合快速出基线。
- **R2 微调（LoRA/全参数）**：gRNA 效率/脱靶二分类、启动子二分类等，用预训练权重 + 分类头微调。
- **R3 长上下文**：HyenaDNA（最长 1M nt）/NT-v2（12 kb）建模"启动子+操纵子+ORF"长区域与变异效应。

**适用场景**：gRNA on/off-target 分类、启动子/TERM/RBS 元件识别、基因表达预测、变异效应（embedding 相减）、靶基因优先级打分。

## 1. 公共数据库与资源原件

| 数据/模型/工具 | 来源 | 获取方式 | 用途 | 注册/授权 |
|---|---|---|---|---|
| DNABERT-3/4/5/6 预训练权重 | GitHub jerryji1993/DNABERT（本地 `repos/DNABERT-master`） | HuggingFace：`zhihan1996/DNA_bert_3`~_`6` | k-mer MLM 底座（3/4/5/6-mer） | 免费，无需注册 |
| DNABERT-2-117M | HF `zhihan1996/DNABERT-2-117M`（本地 `repos/DNABERT_2-main`） | `AutoModel.from_pretrained(..., trust_remote_code=True)` | BPE 多物种底座（推荐默认） | 免费 |
| NT v1/v2 系列 | instadeepai/nucleotide-transformer（本地 `repos/nucleotide-transformer-main`）；HF collection：huggingface.co/collections/InstaDeepAI/nucleotide-transformer-65099cdde13ff96230f2e592 | JAX：`get_pretrained_model(model_name="250M_multi_species_v2", ...)`；PyTorch 走 transformers | 6-mer 分词、12 kb 上下文，变异效应最强（NT-v2 AUC 0.73） | 免费（CC BY-NC-SA 4.0） |
| HyenaDNA tiny~large | HF `LongSafari/hyenadna-{tiny-1k,tiny-16k-d128,small-32k,medium-160k,medium-450k,large-1m}-seqlen`（本地 `repos/hyena-dna-main`） | HF remote code 加载；或本地 `standalone_hyenadna.py` | 单碱基分辨率、最长 1M nt，长上下文首选 | 免费 |
| Caduceus-Ph | HF `kuleshov-group/caduceus-Ph-32M` 等（文献卡 A_Benchmarking…） | transformers 加载 | SSM 双向 + 反向互补等变，RC 对 gRNA 双链友好 | 免费（**需查证具体 HF ID**） |
| GROVER | HF InstaDeepAI grover 系列（文献卡） | transformers 加载 | BPE 人类底座（**需查证 HF ID**） | 免费 |
| GUE 基准（28 数据集×7 任务×4 物种） | DNABERT-2 README Google Drive 链接 | `finetune/scripts/run_dnabert2.sh` 一键评测 | 多物种基因组理解基准 | 免费 |
| dna_foundation_benchmark_dataset | HF `hfeng3/dna_foundation_benchmark_dataset`（文献卡） | HF datasets | 57 数据集零样本嵌入基准（表达部分需 GTEx 授权） | 部分需申请 |
| E. coli K-12 MG1655 参考基因组 | NCBI RefSeq `GCF_000005845.2`；Ensembl Bacteria | NCBI Datasets / Ensembl FTP | 序列提取、gRNA 靶区构造、自训 MLM 数据 | 免费 |
| RegulonDB v10.5+ | regulondb.ccg.unam.mx | 官网下载 | 启动子/TFBS/调控网络注释 | 免费 |
| EcoCyc | ecocyc.org | 官网 | 代谢通路/基因注释（β-丙氨酸、高丝氨酸通路） | 学术免费 |
| CHANGE-seq / GUIDE-seq 脱靶数据 | Lazzarotto 2020 (Nat Biotechnol)、Yaish 2024 (NAR)；GEO GSE149363（表观特征） | 原文献/GEO | 脱靶模型训练与评测 | 免费 |
| CRISPR_DNABERT 代码 | github.com/kimatakai/CRISPR_DNABERT（文献卡） | git clone | DNABERT 脱靶微调 + 5 个基线重实现 | 免费 |
| Genos 1.2B/10B | github.com/BGI-HangzhouAI/Genos；HF `BGI-HangzhouAI` | transformers 4.52.4+ | 1 Mb 上下文 MoE 底座（人类为主，细菌需迁移验证） | MIT，免费 |
| DNABERT-2 预训练数据（135 物种） | DNABERT-2 README Google Drive | 官网链接 | 自训/增量预训练参考 | 免费 |

## 2. 生信处理代码参考（本地仓库提取）

### 2.1 DNABERT（k-mer 预训练）
- **k-mer 转换**：`DNABERT-master/motif/motif_utils.py` 中 `seq2kmer(seq, k)` 把 `ACGT...` 转为 `"ACG CGT GTA ..."`（空格分隔）。微调数据为 TSV：表头 `sequence\tlabel`，见 `examples/sample_data/ft/6/train.tsv`（示例：100 bp 序列 → 95 个 6-mer token）。
- **微调命令**（`examples/run_finetune.py`）：
```bash
export KMER=6 MODEL_PATH=/path/to/DNA_bert_6 DATA_PATH=sample_data/ft/$KMER
python run_finetune.py --model_type dna --tokenizer_name=dna$KMER \
  --model_name_or_path $MODEL_PATH --task_name dnaprom --do_train --do_eval \
  --data_dir $DATA_PATH --max_seq_length 100 --per_gpu_train_batch_size 32 \
  --learning_rate 2e-4 --num_train_epochs 5.0 --output_dir ./ft/$KMER \
  --warmup_percent 0.1 --hidden_dropout_prob 0.1 --weight_decay 0.01 --n_process 8
```
  预测用 `--do_predict --predict_dir ...`；多 k-mer 集成用 `--do_ensemble_pred`（k=3/4/5/6）。
- **预训练**：`examples/run_pretrain.py`，`--mlm --block_size 512 --mlm_probability 0.025 --learning_rate 4e-4 --max_steps 200000`（README 原始参数），输入为逐行序列文件（`sample_data/pre/6_3k.txt`）。

### 2.2 DNABERT-2（BPE 多物种，推荐默认）
嵌入提取（README 官方示例，mean pooling 优于 CLS，见 §4）：
```python
from transformers import AutoTokenizer, AutoModel
import torch
tok = AutoTokenizer.from_pretrained("zhihan1996/DNABERT-2-117M", trust_remote_code=True)
model = AutoModel.from_pretrained("zhihan1996/DNABERT-2-117M", trust_remote_code=True)
dna = "ACGTAGCATCGGATCTATCTATCGACACTTGGTTATCGATCTACGAGCATCTCGTTAGC"
inputs = tok(dna, return_tensors="pt")["input_ids"]
hidden = model(inputs)[0]                      # [1, L, 768]
emb = torch.mean(hidden[0], dim=0)             # mean pooling → 768 维
```
微调数据为 CSV（表头 `sequence,label`，单序列或双序列分类均可，见 `finetune/train.py` 的 `SupervisedDataset`）；训练入口 `finetune/train.py`（transformers Trainer + LoRA，见 §3）。

### 2.3 Nucleotide Transformer v2
JAX 官方 API（`nucleotide-transformer-main`）：`get_pretrained_model(model_name="250M_multi_species_v2", embeddings_layers_to_save=(20,), max_positions=32)`，输出 `outs["embeddings_20"]`；层号 1 起始，取最后层后接 LM head 第一层 LN 的嵌入更佳。分词规则：6-mer 从左到右，遇 `N` 或长度非 6 倍数则单碱基切分；v2 最长 12,282 nt（2,048 token）。PyTorch 用法与 LoRA 微调参考 HF notebook：`huggingface/notebooks/examples/nucleotide_transformer_dna_sequence_modelling_with_peft.ipynb`。

### 2.4 HyenaDNA（长上下文）
本地 `hyena-dna-main/standalone_hyenadna.py` 含完整模型定义 + 微调示例（Hyena 层核心：`fftconv` 频域长卷积）；也可 HF remote code 加载 `LongSafari/hyenadna-medium-450k-seqlen` 等。仓库内训练入口：`python -m train wandb=null experiment=hg38/genomic_benchmark_scratch`（Pytorch Lightning + Hydra 配置驱动）。

### 2.5 环境依赖
- DNABERT：Python 3.6 + torch(CUDA 10.0)，`pip install --editable .`（旧 transformers API，需 py3.6 环境，**如需在 py3.10+ 运行需查证兼容性**）。
- DNABERT-2：`requirements.txt` 固定 `transformers==4.29.2, peft==0.3.0, torch==1.13.1, accelerate==0.20.3, einops, scikit-learn`。
- NT：JAX 生态（haiku、flax）；PyTorch 版走 transformers。
- HyenaDNA：torch 1.13 + cuda 11.7 + flash-attention 子模块（或 Docker：`docker pull hyenadna/hyena-dna:latest`）。

## 3. 大模型训练代码（微调骨架，PyTorch 优先）

数据预处理（E. coli gRNA 效率/启动子二分类）：取 gRNA 靶点侧翼序列（建议 PAM 上游 30 bp + 下游 30 bp 共 ~60 bp；元件任务取启动子 ±150 bp），造 CSV/TSV。注意 DNABERT-2 的 `--model_max_length` 设 0.25×序列长度（BPE 约 5 倍压缩）；DNABERT k-mer 需先 `seq2kmer`。

```python
# 依赖: transformers, peft, torch, sklearn (DNABERT-2 requirements 已验证版本)
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType

MODEL = "zhihan1996/DNABERT-2-117M"   # 或 NT-v2 / HyenaDNA HF ID
tok  = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2, trust_remote_code=True)

# LoRA（DNABERT-2 finetune/train.py 同款参数）
lora = LoraConfig(task_type=TaskType.SEQ_CLS, r=8, lora_alpha=32,
                  lora_dropout=0.05, target_modules=["query", "value"])
model = get_peft_model(model, lora)
model.print_trainable_parameters()      # 预期仅 ~0.1-1% 可训练

args = TrainingArguments(
    output_dir="./ft_grna", learning_rate=3e-5, num_train_epochs=5,
    per_device_train_batch_size=8, gradient_accumulation_steps=1,
    warmup_steps=50, fp16=True, evaluation_strategy="steps", eval_steps=200,
    save_steps=200, logging_steps=100, load_best_model_at_end=True)
Trainer(model=model, args=args, train_dataset=train_ds,
        eval_dataset=dev_ds, compute_metrics=compute_metrics).train()
```

**训练超参数建议（文献卡原始参数）**：DNABERT-2 微调 lr=3e-5、epochs 3–5、batch 8（全局 32 复现 GUE）；DNABERT 微调 lr=2e-4、epochs 5；DNABERT 预训练 lr=4e-4、mlm_prob=0.025、block 512、200k steps；脱靶两阶段微调（阶段一错配位置预测 lr=2e-5、阶段二分类 lr=2e-5，见 DNABERT-Epi 文献卡）。评估协议：按 sgRNA 分组 10 折 CV + 5 随机种子 + Wilcoxon 检验；极端不平衡负类降采样至 20%（固定种子）；指标 F1/MCC/AUROC/PR-AUC；AUROC 显著性用 DeLong 检验。

**自训练 MLM 底座（可选）**：用 E. coli 全基因组切片做 k-mer 序列文件，`run_pretrain.py` 复现 DNABERT 预训练管线；或对 DNABERT-2 做细菌基因组增量预训练（**需查证其官方增量训练脚本**）。

## 4. 解释文档（中文）

**方法原理**：DNA 预训练模型把基因组当作"语言"：DNABERT 用 k-mer 分词 + BERT MLM（遮盖 15% 左右 token 预测还原）；DNABERT-2 改用 BPE（词表学习、序列压缩约 5 倍）+ ALiBi 位置编码（免学习式、外推性好），多物种（135 物种）预训练；NT-v2 用 6-mer 分词 + RoPE 旋转位置编码 + SwiGLU 门控激活，去 bias/dropout，2,048 token 窗口；HyenaDNA 用 Hyena 算子（隐式参数化长卷积 + 频域 FFT 卷积，替代 attention，线性复杂度）实现单碱基分辨率 1M token 上下文；Caduceus-Ph 为双向状态空间模型（MambaDNA + 反向互补等变）。

**关键结论（benchmark 对比）**：
- **池化**：mean token pooling 稳定优于 [CLS]/max（52 个二元任务中 DNABERT-2 41 个、NT-v2 42 个、HyenaDNA 35 个显著；summary→mean AUC 提升 1.4%–8.7%），且缩小模型间差距（AUC 跨度 0.708–0.799 → 0.795–0.822）——工程上默认 mean pooling。
- **选型**：长序列（>12 kb，操纵子/长调控区）选 HyenaDNA；中等（≤12 kb）选 NT-v2/Caduceus-Ph；短元件分类 Caduceus-Ph 与 DNABERT-2 最强；变异效应 NT-v2 最佳（AUC 0.73）；基因表达零样本嵌入只有 r≈0.12，需微调或专用模型。
- **迁移风险**：基准全部基于人/多物种真核，细菌启动子任务上 foundation 模型普遍输给任务专用 CNN（R. capsulatus 最高仅 0.715），E. coli 上必须自测"基线 CNN vs 冻结嵌入"。

**gRNA 任务应用**：DNABERT（3-mer）两阶段微调（先错配位置预测、再脱靶二分类）+ 表观特征融合（DNABERT-Epi）在 CHANGE-seq/GUIDE-seq 上 SOTA（ROC-AUC 0.9187）；消融证明预训练不可替代。我们的 gRNA 效率/脱靶任务可直接套用：输入 [CLS]+DNA 侧翼 3-mer+[SEP]+sgRNA 3-mer+[SEP]；DNABERT-2/NT-v2 的 mean pooling 嵌入作为效率回归/分类特征；脱靶量化用 embedding(错配靶点)−embedding(参考) 效应向量。

**与课题关联**：大肠杆菌基因组仅 4.64 Mb、~4,400 基因，嵌入成本极低——可用全基因组扫描生成"启动子/操纵子/基因级"嵌入库；β-丙氨酸/高丝氨酸通路基因（如 aspC、panD、thrA 相关操纵子）的靶基因优先级可复用 DVPNet 的"TSS 锚定（−2000/+500 bp）+ 平均池化 + 贡献打分"范式；调控元件识别（启动子/TERM/RBS）为 gRNA 设计提供打靶坐标。

**常见坑**：① DNABERT 旧版 transformers API 与新版本不兼容，建议独立 conda 环境；② 加载 DNABERT-2/NT/HyenaDNA 需 `trust_remote_code=True`；③ k-mer 序列长度 ≠ 碱基长度，max_seq_length 按 token 计；④ 同 sgRNA 的位点必须同折划分（数据泄漏）；⑤ 大肠杆菌 GC 50.8% 与人类差异大，BPE/6-mer 分词覆盖率需验证，必要时增量预训练；⑥ LoRA target_modules 需匹配模型实际模块名（DNABERT-2 为 `query,value`，其他模型需查证）。

## 5. 行动项（可直接落地）

1. **【P0】E. coli gRNA 侧翼序列嵌入基线**：用 DNABERT-2-117M 与 NT-v2-250M 对 gRNA 靶区（±60 bp）生成 mean-pooling 嵌入 → 随机森林，在公开效率数据（DeepCRISPR/CRISPRon 数据）上出 AUROC/F1 基线，与 DeepCRISPR 原模型对比（复用 `repos/DeepCRISPR-master`）。
2. **【P0】池化消融与元件分类**：启动子/TERM/RBS 二分类任务上跑 3 模型 × 3 池化消融，确认 mean pooling 在细菌上的收益；用 E. coli K-12 MG1655 + RegulonDB 注释构建数据集。
3. **【P1】LoRA 微调 gRNA 效率模型**：按 §3 骨架用 peft 微调 DNABERT-2（两阶段：错配位置→二分类），评估协议采用按 sgRNA 分组 10 折 CV + 负类降采样；与冻结嵌入基线对比。
4. **【P1】脱靶效应向量**：实现 embedding(错配靶点)−embedding(参考序列) 特征，与错配数/PAM 得分融合，接随机森林分类（借鉴染色体分组嵌套 CV，E. coli 按复制起点/基因岛分组）。
5. **【P2】长上下文建模**：对"启动子+操纵子+ORF"（≤12 kb）用 HyenaDNA-450K/NT-v2 提取区域嵌入，做基因表达/编辑效果预演特征；并把"mean pooling 优先、按 sgRNA 分组 CV、统一浅层头评测"写入 README 工程规范。

**待查证项**：Caduceus-Ph/GROVER 的精确 HF 模型 ID 与 PyTorch 加载代码；DNABERT-2 官方增量预训练脚本；E. coli 专属 gRNA 效率湿实验数据集规模（建议以体外 CHANGE-seq/CIRCLE-seq 或 Cas-OFFinder 候选 + 少量验证构建）。
