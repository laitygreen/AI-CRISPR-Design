# RouteD：LLM 与 Agent 方法包（BioGPT 微调 / D2Cell 复刻 / CRISPR-GPT Agent / RAG / LoRA / 指令数据集）

> 适用：本路线为 AI-CRISPR 系统提供"大脑"：让机器**读文献 → 建知识库 → 推荐靶点 → 设计 gRNA → 解释决策**。
> 依据文献卡：S_BioGPT（LLM 底座）、S_D2Cell（LLM 文献挖掘 + GEM+GNN 预测 + RAG）、S_Cas12a-LLM（蛋白 LLM + 小样本活性预测）；本地仓库：DNABERT / DNABERT-2（序列底座与 LoRA 微调模板）。**BioGPT / D2Cell / CRISPR-GPT / BioT5 无本地仓库，以 GitHub 链接 + 文献卡为准。**

## 0. 路线总览

**解决什么问题**：AI-CRISPR 系统需要把海量代谢工程/CRISPR 文献转成可计算的知识（基因-酶-产物-调控关系），并回答"打哪个基因、用什么 gRNA、为什么"这类设计问题。传统手工整理不可扩展，通用 LLM（GPT-2/GPT-3）存在领域偏移、缺乏 E. coli 代谢与 CRISPR 专门知识（BioGPT 文献卡证据）。

**子路线（多途径，可并行）**：

| 编号 | 子路线 | 关键方法 | 对应文献卡/仓库 |
|---|---|---|---|
| D1 | 领域 LLM 底座 | BioGPT 微调、关系抽取、PubMedQA | microsoft/BioGPT |
| D2 | LLM 文献挖掘管线 | NER→RE→ER 任务分解，构建 29,006 条工程库 | LiLabTsinghua/D2Cell |
| D3 | 知识+预测混合模型 | D2Cell-pred：GEM(iML1515)+GNN+LLM 靶点预测 | D2Cell / cobrapy（本地） |
| D4 | CRISPR-GPT Agent 架构 | 多智能体：实验规划→设计排序→gRNA 文库→模拟验证 | cong-lab/crispr-gpt-pub |
| D5 | RAG 问答 + 微调基建 | BGE-M3 向量化 + LangChain；LoRA 微调；指令数据集 | D2Cell RAG / DNABERT-2 |

**适用场景**：文献自动摘要与关系抽取、靶点推荐的可解释性、gRNA 设计问答、实验方案自动生成、菌株-产物-编辑记录库的自动入库。

## 1. 公共数据库与资源原件

| 数据/模型/工具 | 来源 | 获取方式 | 用途 | 授权 |
|---|---|---|---|---|
| BioGPT 代码+权重（347M/Large） | microsoft/BioGPT | https://github.com/microsoft/BioGPT | 领域 LLM 微调/关系抽取底座 | 开源（MIT） |
| D2Cell 全量代码+29,006 条数据库 | 论文：Leveraging LLMs for Metabolic Engineering Design（bioRxiv 2024.09.09.612023） | 论文：https://www.biorxiv.org/content/10.1101/2024.09.09.612023 ；代码以论文页面链接为准（文献卡记录为 https://github.com/LiLabTsinghua/D2Cell ，**需查证**） | 工程记录库、NER/RE prompt、D2Cell-pred | 开源（预印本未同行评审） |
| CRISPR-GPT | cong-lab/crispr-gpt-pub | https://github.com/cong-lab/crispr-gpt-pub | Agent 架构参考（现为公开欢迎页，核心代码是否开放**需查证**） | 论文 Nature Biomedical Engineering 2025 |
| BioT5 / BioT5+ | QizhiPei/BioT5 | https://github.com/QizhiPei/BioT5 | 跨模态（分子+蛋白+文本）LLM 底座 | 开源（用户猜测的 tongzhou21/BioT5 **需查证**，实为 QizhiPei/BioT5） |
| DNABERT（k-mer BERT） | jerryji1993/DNABERT | 本地 `repos/DNABERT-master` | 序列级预训练/微调参考 | 开源 |
| DNABERT-2（BPE 多物种） | MAGICS-LAB/DNABERT_2 | 本地 `repos/DNABERT_2-main`（权重在 HuggingFace zhihan1996/DNABERT-2-117M） | 序列分类微调 + **LoRA 微调现成模板** | 开源 |
| PubMed 摘要语料 | NCBI | https://ftp.ncbi.nlm.nih.gov/pubmed/ | 预训练/继续预训练语料 | 公开 |
| PubMedQA / BC5CDR / KD-DTI / DDI | 公开基准 | BioGPT 仓库 `examples/` 内脚本自动下载 | 抽取/问答评测 | 公开 |
| IEPile 指令集 | zjunlp/IEPile | https://github.com/zjunlp/IEPile | 信息抽取指令数据（防灾难性遗忘） | 开源 |
| LASER 菌株工程库 | jdwinkler/laser_release | https://bitbucket.org/jdwinkler/laser_release/ | D2Cell-pred 独立测试集 | 需查证 |
| E. coli GEM iML1515 | BiGG | http://bigg.ucsd.edu/models/iML1515 | GEM 约束模拟/FSEOF | 公开 |
| UniProt / NCBI Taxonomy / KEGG / PubChem | 各官网 | REST API | 实体归一化（基因/菌株/化合物 ID） | 部分需 API key |
| EcoCyc / RegulonDB | 官网 | https://ecocyc.org / https://regulondb.ccg.unam.mx | E. coli 基因/调控知识 | 需注册（学术免费） |

> ✅ **已核实官方链接**：BioGPT → https://github.com/microsoft/BioGPT ；BioT5/BioT5+ → https://github.com/QizhiPei/BioT5 ；CRISPR-GPT → https://github.com/cong-lab/crispr-gpt-pub ；D2Cell → 论文 https://www.biorxiv.org/content/10.1101/2024.09.09.612023 （bioRxiv 2024.09.09.612023），代码入口以论文页面为准。

## 2. 生信处理代码参考

### 2.1 本地可直接使用的代码（DNABERT / DNABERT-2）

- **DNABERT-2 微调**（含 LoRA，最贴近本路线）：`repos/DNABERT_2-main/finetune/train.py`
  - 关键 API：`peft.LoraConfig`（`lora_r=8, lora_alpha=32, lora_dropout=0.05, target_modules="query,value"`）、`get_peft_model`、`transformers.Trainer`；数据为 CSV（`seq,label` 两列），内置 `load_or_generate_kmer` 将 DNA 转 k-mer 字符串（`generate_kmer_str(seq, k)`）。
  - 运行示例（真实命令，来自仓库 README/脚本）：
    ```bash
    conda create -n dnabert2 python=3.9 && conda activate dnabert2
    pip install transformers==4.29.2 peft==0.3.0 torch==1.13.1 accelerate==0.20.3 scikit-learn==1.2.2 evaluate==0.4.0
    python finetune/train.py \
      --model_name_or_path zhihan1996/DNABERT-2-117M \
      --data_path data/grna_train.csv --kmer -1 \
      --use_lora --lora_r 8 --lora_alpha 32 \
      --per_device_train_batch_size 16 --learning_rate 1e-4 \
      --num_train_epochs 10 --max_seq_length 512 --output_dir output_grna
    ```
    输入：`data/grna_train.csv`（列 `seq`：23 bp sgRNA 或 30 bp 上下文序列；列 `label`：0/1 效率标签）；输出：LoRA 微调权重 + eval 指标。
- **DNABERT 预训练/微调命令**：`repos/DNABERT-master/examples/run_pretrain.py`、`run_finetune.py`（kmer=3~6，MLM 目标，`--mlm_probability 0.025`、`--learning_rate 4e-4`、`--max_steps 200000` 为官方默认）；k-mer 转换函数在 `motif/motif_utils.py` 的 `seq2kmer`。

### 2.2 远程仓库代码路径（需 git clone）

- **D2Cell**（论文：Leveraging LLMs for Metabolic Engineering Design，bioRxiv 2024.09.09.612023，https://www.biorxiv.org/content/10.1101/2024.09.09.612023 ；文献卡记录的仓库为 `git clone https://github.com/LiLabTsinghua/D2Cell`，**需查证**）：重点看 `prompts/`（NER/RE 的 few-shot prompt 原文）、数据导出脚本（29,006 条记录的字段：organism/product/titer/gene_modification/medium/temperature/volume/DOI）、D2Cell-pred 训练脚本（GNN 部分基于 PyTorch Geometric，具体文件名以 clone 后为准，**需查证**）。
- **BioGPT**（`git clone https://github.com/microsoft/BioGPT`）：顶层 `run_lm_finetune.py`、`run_lm_pretrain.py`，`examples/` 下按任务分子目录（relation_extraction / qa_finetune / text_generation / document_classification，子目录脚本名以仓库为准，**需查证**）；PubMed 预处理脚本在 `MEDLINE-PubMed-Baseline/` 目录。权重经 `huggingface-cli download microsoft/biogpt` 或仓库内下载链接获取。

### 2.3 数据格式约定（对齐 D2Cell 字段，直接服务入库）

每条工程记录最小字段集：`organism | strain_id | product | titer(g/L) | gene_modification(增/减/敲除) | medium | temperature | volume | O2 | DOI`——这是后续训练与 RAG 检索的统一 schema（D2Cell 文献卡第 5.7 条）。

## 3. 大模型训练代码

### 3.1 指令数据集构建（D5，伪代码可跑）

把知识库记录改写成"指令-输入-输出"三元组（对齐 BioGPT"标签→自然语言目标"范式）：

```python
# build_instruction_data.py
import json, csv
recs = list(csv.DictReader(open("knowledge_base.tsv", encoding="utf-8")))
data = []
for r in recs:
    data.append({
        "instruction": "根据文献，{product} 生产中，{organism} 菌株 {strain} 的基因改造是什么？",
        "input": f"产物={r['product']}; 菌株={r['strain_id']}",
        "output": (f"改造基因: {r['gene_modification']}；滴度: {r['titer']} g/L；"
                   f"培养基: {r['medium']}；来源: {r['DOI']}"),
        "source": r["DOI"],
    })
json.dump(data, open("instruct_d2cell.json", "w", encoding="utf-8"), ensure_ascii=False)
# 混合 IEPile 通用抽取样本(约 20k)防止灾难性遗忘，比例建议 1:2~1:5
```

### 3.2 LoRA 微调骨架（PyTorch + transformers.Trainer，基于 DNABERT-2 仓库代码）

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType

model = AutoModelForSequenceClassification.from_pretrained("zhihan1996/DNABERT-2-117M", num_labels=2)
tokenizer = AutoTokenizer.from_pretrained("zhihan1996/DNABERT-2-117M")
lora = LoraConfig(task_type=TaskType.SEQ_CLS, r=8, lora_alpha=32,
                  lora_dropout=0.05, target_modules=["query", "value"])
model = get_peft_model(model, lora)   # 仅训练 ~1% 参数

args = TrainingArguments(output_dir="out_grna", per_device_train_batch_size=16,
    learning_rate=1e-4, num_train_epochs=10, fp16=True,
    gradient_accumulation_steps=4, save_total_limit=3, load_best_model_at_end=True)
trainer = Trainer(model=model, args=args,
    train_dataset=train_ds, eval_dataset=val_ds, compute_metrics=compute_metrics)
trainer.train()
trainer.save_model("out_grna_lora")   # 推理时 model.load_adapter("out_grna_lora")
```
注：`train_ds` 需实现 `__getitem__` 返回 `{"input_ids": tok(seq)["input_ids"], "labels": label}`；DNA 序列直接用 BPE 字符 tokenizer（kmer=-1），无需 3-mer 切分——这是 DNABERT-2 相对 DNABERT 的主要简化。

### 3.3 BioGPT 微调（文献任务，命令 + 超参）

- 任务改写格式（**rel-is 格式**，BioGPT 验证最优）：目标序列 = `the relation between <head> and <tail> is <relation>`；多三元组用分号拼接；问答前缀 `question: ... context: ...`。
- 命令骨架（真实脚本名，参数来自文献卡）：`python run_lm_finetune.py --model_name_or_path microsoft/biogpt --do_train --train_data_file train.jsonl --max_steps 100000 ...`（具体参数名以仓库 README 为准，**需查证**）。
- 超参数（文献卡原始值）：微调 LR 1e-5~1e-4，30~100 epochs，batch=1024 token×32 梯度累积；软提示长度 9~13，插在 source 与 target 之间；评测取最后 5 epoch 平均，生成用 beam=5。

### 3.4 D2Cell-pred 复刻骨架（GEM+GNN，伪代码）

```python
# 输入: 目标产物 e_product、基因改造集合 G、iML1515 图 G_net(代谢物节点/反应边)
from torch_geometric.nn import GCNConv
class D2CellPred(torch.nn.Module):
    def __init__(self, emb_dim=128):
        super().__init__()
        self.gnn1 = GCNConv(emb_dim, emb_dim); self.gnn2 = GCNConv(emb_dim, emb_dim)
        self.gene_mlp = torch.nn.Linear(emb_dim, emb_dim)   # 多基因嵌入求和→MLP
        self.final = torch.nn.Linear(3*emb_dim, 2)          # [gene‖product‖graph]→二分类
    def forward(self, x_met, edge_index, x_gene_sum, e_product, x_graph):
        e_met = self.gnn2(torch.relu(self.gnn1(x_met, edge_index)), edge_index)
        z = torch.cat([self.gene_mlp(x_gene_sum), e_product, x_graph], dim=-1)
        return self.final(z)   # 交叉熵，正:负=40:60
# 训练数据: E.coli 19,777 条 = 8,134 实验(单/双基因) + 11,643 FSEOF 模拟; cobrapy 跑 FSEOF:
#   from cobra.flux_analysis import pfba; 对 iML1515 逐基因过表达/敲除扫描强制目标函数(见 cobrapy 文档)
```

## 4. 解释文档（中文）

**为什么需要领域 LLM**：通用 LLM 在生物医学上表现差是"领域偏移"——词表与知识分布不匹配（BioGPT 引 PubMedBERT 结论）。解决方案三选一：①域内从零预训练（BioGPT，成本高）；②通用模型 + 领域微调/LoRA（D2Cell 路线，性价比最高）；③RAG 外挂知识（最便宜，用于问答）。

**BioGPT 的生成式统一范式**：把所有任务（抽取/分类/问答）改写为"自然语言目标序列"，用同一个自回归解码器输出；软提示（prefix-tuning 连续向量）插在 source 与 target 之间优于放开头。启示：我们让 LLM 输出 gRNA 设计时，也可用 "the predicted cleavage efficiency of guide X is <label>" 式文本目标，或用 JSON 结构化输出。

**D2Cell 为什么把任务分解成 NER→RE→ER**：一次性 prompt 抽取精度低（端到端 74~79% vs 直接抽取多提 50~100% 数据）；14B+LoRA 做 NER（F1 86%），110B 长上下文模型做 RE（32k token 读全文，Llama-3 因 8k 上限被淘汰），再用 UniProt/KEGG API 归一化实体 ID。**教训：按"任务复杂度×上下文长度×成本"选模型，不要一律用最贵的。**

**D2Cell-pred = 机械论 + 数据驱动混合**：GEM（iML1515）提供机制约束并生成 FSEOF 模拟数据补足实验数据稀缺；GNN 把 GEM 当图做消息传递；产物嵌入与 GEM 代谢物共享；多基因改造求和聚合。消融证明"图级全局特征"对多基因组合预测关键。这与我们"先 D2Cell 出靶点 → 再 gRNA 模型出编辑方案"是分层串联关系。

**CRISPR-GPT Agent 架构**（Nature Biomedical Engineering 2025）：四模块多智能体——①实验规划与设计（选靶基因）②CRISPR 设计排序（PAM、on/off-target 评分）③gRNA 文库构建与实验方案④模拟与验证；强调人机协作（每步人工审核）。我们的 demo 可按此搭一个简化版：用户输入"目标产物 β-丙氨酸"→ Agent 查知识库 → 调 gRNA 效率模型 → 输出 gRNA 列表 + 实验方案（附文献 DOI）。

**RAG 知识库**：BGE-M3 多语言嵌入把 29,006 条表格记录向量化，查询取 top-5 相似条目拼进 prompt，回答附 DOI 溯源（减少幻觉）。LangChain 实现，架构可直接照搬。

**LoRA 与常见坑**：LoRA 只训练低秩增量矩阵（r=8），显存/算力省 90%+，适配快速迭代。坑点：①幻觉——回答必须带 DOI 溯源，必要时规则校验；②文献偏置——文献只报成功改造，训练负样本需构造（与增产相反改造 + FSEOF 未预测靶点，正:负=40:60）；③灾难性遗忘——微调时混入 IEPile 通用抽取样本；④实体归一化——菌株名不规范（"QW101"），必须映射 UniProt/KEGG/NCBI ID；⑤语料时效——BioGPT 语料截止 2021，CRISPR 新技术知识要增量补充；⑥小样本——Cas12a 活性预测用"ESM 嵌入+PCA 降维 4~8 维+树模型"在 69 样本上达 92.3%，可直接迁移到 gRNA 小样本场景。

**与课题关联**：β-丙氨酸（天冬氨酸-α脱羧酶 panD 通路）与 L-高丝氨酸（天冬氨酸激酶 thrA/metL、高丝氨酸脱氢酶 hom/thrA 分支）的"基因-酶-产物"关系正是 D2 抽取的目标；D2Cell-pred 可直接以这两种产物为 label 训练靶点预测；RAG 问答即系统 D 模块的 MVP。

## 5. 行动项（按优先级）

1. **[P0] 复刻 D2Cell-learn 三步管线，构建 β-丙氨酸/高丝氨酸知识库**：clone LiLabTsinghua/D2Cell，用其 NER/RE prompt + Qwen1.5-14B-Chat LoRA 微调，对 PubMed 相关文献抽取"基因改造→产物→滴度"，实体用 UniProt/KEGG 归一化，按第 2.3 节 schema 入库。产出：100~500 条带 DOI 的氨基酸工程记录（支撑 B1/M4）。
2. **[P0] 搭建 RAG 问答 MVP**：BGE-M3 + LangChain + top-5 检索 + Qwen/DeepSeek 生成，回答附 DOI；用第 3.1 节指令数据集 + 知识库向量化。产出：可演示的"代谢工程知识问答"（项目亮点）。
3. **[P1] 复现 D2Cell-pred（iML1515 + GNN）做靶点预测基线**：用本地 cobrapy 跑 FSEOF 生成模拟数据，按第 3.4 节骨架训练，与 RouteA gRNA 模型串联成"靶点→gRNA"端到端流水线。
4. **[P1] DNABERT-2 + LoRA 微调 gRNA 效率/脱靶模型**：把 RouteA 的数据转成 CSV（seq,label），用第 3.2 节骨架训练；同时复刻"ESM 嵌入+PCA+LightGBM"小样本配方做对照（借鉴 S_Cas12a 卡）。
5. **[P2] CRISPR-GPT 式多智能体 demo**：输入"目标产物+底盘"→ 检索知识库 → 调靶点模型 → 调 gRNA 模型 → 输出设计方案；以此驱动指令数据集扩充，制作端到端演示视频。

> **推进节奏**：P0（知识库 + RAG MVP）；9 月中完成 P1 基线复现与微调；P2 完成 demo 与文档收尾。所有 GitHub 资源先 clone 到 methods/repos/ 再离线使用。
