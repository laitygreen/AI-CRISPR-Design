---
# 文献卡：Genos: a human-centric genomic foundation model

| 字段 | 内容 |
|---|---|
| 分级 | A |
| 主题 | T4 LLM与Agent（基因组基础模型） + T3 DNA底座（超长序列建模） |
| 年份 | 2025 |
| 期刊 | GigaScience, Vol. 14, pp. 1–13 |
| DOI | 10.1093/gigascience/giaf132 |
| 项目映射 | M4（LLM/基因组基础模型，可直接微调复用）；M3（DNA底座：超长上下文、单碱基分辨率）；B1（MoE 训练/部署工程经验） |

## 1. 一句话核心
Genos 是面向人类的基因组基础模型（Genos-1.2B / Genos-10B，MoE 架构），通过多来源高质量单倍型组装（HPRC+HGSVC+CEPH，636 个人类基因组）与渐进式超长上下文训练实现 1 Mb 上下文的单碱基分辨率建模，在 Genomics/Nucleotide Transformer/Long-Range 基准上全面超越现有 SOTA，并展示从 DNA 序列预测单碱基 RNA-seq 表达谱与"基因组+文本"跨模态疾病诊断能力。

## 2. 方法要点（详细）
- **数据工程**：636 个高质量人类基因组 = 231 个 HPRC release 2 单倍型组装 + 65 个 HGSVC + 21 个 CEPH + 2 个参考基因组（GRCh38、CHM13）；one-hot 分词（A/T/C/G/N + 特殊 token，如 <EOD>）；预训练阶段**不加任何表观/功能注释标签**（无偏表示）；多级质控管线过滤不同长度基因间序列（含 segmental duplication）。
- **预训练策略**：两阶段——① 预训练：按 3:3:3:1 比例将 HPRC 样本分为 8,192 / 32,768 / 131,072 / 1,024,000 bp 四组（约 1.4T tokens），每组约 1/4 样本双单倍型反转互补；8K 片段排除距基因边界 >5,120 bp 的区域，32K 排除 >10,240 bp；② 继续预训练（CPT）：重新混排长度与链向生成 2.6T tokens，**不做任何过滤**（覆盖远端基因间区、SD、转座子等"负背景"序列）；按长度递增顺序喂入。
- **架构**：12 层 MoE Transformer；8 个专家、每 token 激活 top-2（router）；GQA（16 头、8 个 KV 组）；RoPE 基频 50,000,000（支持 1M token）；3 层 RMSNorm；SwiGLU 激活；Flash Attention；NTP 目标；Genos-1.2B：总参 1.25B / 激活 0.33B，hidden 1,024，MoE hidden 4,096，vocab 128；Genos-10B：总参 10.27B / 激活 2.87B，hidden 4,096，MoE hidden 8,192，vocab 256；训练 token：1.2B 版 1,600B，10B 版 2,200B。
- **训练工程**：Megatron-LM + 256 GPUs + 5 维并行（tensor/pipeline/context/data/expert）；global batch 1,024（micro-batch 1）；AdamW + cosine 学习率（5% warmup，峰值 1e-4）+ 梯度裁剪 1.0 + weight decay 0.1；MoE 负载均衡 aux loss（系数 1e-3）+ Z-loss（系数 1e-3）；混合精度：BF16 为主，Softmax/梯度累积与 All-Reduce/MoE routing 保持 FP32；渐进式上下文长度训练 + 计划性 LR 衰减（缓解灾难性遗忘）+ RoPE 上下文窗口缩放；grouped GEMM、all-to-all token dispatch、参数收集与梯度归约重叠、8 worker 循环数据加载。
- **评测**：GB（demo_coding_vs_intergenomic_seqs、human_enhancers_cohn、human_ocr_ensembl）、NTB（splice_sites_all、H3、H3K36me3）、LRB（regulatory_element_enhancer_8K/promoter_8K、variant_effect_causal_eqtl_8K、pathogenic_clinvar_8K，均用 8,192 bp 输入，chr22 作验证集）；自建突变热点分类（Chinese Pangenome Consortium，Poisson 右尾检验 FDR<0.05，8K/32K/128K）；所有任务用序列模型 embedding + 固定简单下游网络评估（公平对比）。
- **RNA-seq 预测案例**：微调 Genos-1.2B；数据 ENCODE+GTEx 共 667 个单碱基转录组样本组；BigWig 归一化后组内平均；输入 hg38、32 kb 窗口（16 kb 重叠）；输出头 3 层 1D 卷积（(kernel,pad,dilation)=(3,1,1),(3,2,2),(1,0,1)，通道 1024→256→64→1）+ BN + GELU + dropout 0.1 + Softplus；MSE 损失；sqrt 平滑裁剪/幂变换（同 AlphaGenome）；Adafactor + cosine annealing（5% warmup）、global batch 256、60 epochs。
- **基因组-文本融合案例**：KEGG 疾病推理任务（1,449 条、37 种疾病，8:1:1 划分，DNA 最长 1,024 bp）；文本模型 Qwen3-1B/4B/8B 与 021-8B；AdamW lr 5e-5、wd 1e-2、梯度累积 8、seed 23；**LoRA rank 32 / α 64 / dropout 0.05，仅微调文本模型、冻结 DNA 模型**。

## 3. 关键结果与指标
- 短序列（200–600 bp）：Genos-10B 在 demo_coding_vs_intergenomic_seqs 达 AUC 0.9914（GENE-Rator-3B 0.9855、HyenaDNA-1M 0.9127、NT-2.5b-multi 0.9763）；human_enhancers_cohn AUC 0.8552（NT-2.5b-multi 0.7873、Evo2-7b 0.7733）。
- 长序列（8K）：regulatory_element_enhancer_8K AUC 0.7532；variant_effect_pathogenic_clinvar_8K AUC 0.9326（GENE-Rator-3B 0.7206、HyenaDNA-1M 0.6117）。
- 突变热点（8–128K）：CPC_131072 AUC 0.9911（GENE-Rator-3B 0.9620、HyenaDNA-1M 0.9735）；CPC_32768 AUC 0.9625；序列越长性能越高（其他模型无法处理 128K 或未表现长度-性能正相关）。
- RNA-seq 预测（Genos-1.2B，log1p Pearson 相关）：GM12878 + 链：全基因组 0.9335、基因区 0.9334、基因表达矩阵 0.8641；− 链：0.9182 / 0.9274 / 0.9081；NK 细胞 + 链：0.9084 / 0.9036 / 0.9267；− 链 0.8562 / 0.8542 / 0.8969。Genos-10B（chr19 初步微调）已优于 AlphaGenome。
- 疾病诊断（KEGG 多标签）：Genos-10B 单独 acc 92.07%、macro F1 72.59%；Genos-1.2B + 021-8B 组合 acc 98.28%、F1 90.37%（结论中称部分场景 acc 达 99.31%）；DNA 模型冻结 + LoRA 微调文本模型即可取得高精度。

## 4. 数据与代码可用性
- 模型权重/推理代码/文档：GitHub https://github.com/BGI-HangzhouAI/Genos；Hugging Face https://huggingface.co/BGI-HangzhouAI；ModelScope https://modelscope.cn/organization/BGI-HangzhouAI。
- 许可：**MIT**（可自由商用/修改/再分发）；Python，要求 transformers 4.52.4+（原文称 "pytorch 7.1 or higher"，疑为笔误）；DCS-Cloud 提供云端推理 API。
- 训练数据来源公开：HPRC（BioProject PRJNA698480）、HGSVC、CEPH、GRCh38/CHM13、ENCODE/GTEx、KEGG。

## 5. 对我们项目的可借鉴点（重点，结合大肠杆菌氨基酸细胞工厂 + AI-CRISPR 设计）
1. **"DNA 编码器冻结 + 文本 LLM LoRA 微调"的多模态融合架构可直接复用（M4）**：Genos 的基因组-文本融合案例证明，冻结基因组模型、仅用 LoRA（rank 32/α 64）微调文本 LLM 即可在"序列+自然语言"任务上达到高精度（acc 98.28%）——我们的 LLM-Agent 模块（如"给定目标产物 β-丙氨酸，生成改造方案"）可照搬该架构：DNA 嵌入编码器（可用 Genos 或小型 DNA BERT）提供序列表示，Qwen 等 LLM 负责推理与方案生成。
2. **RNA-seq 预测范式 → "gRNA 设计的效果预演"（M1/M4 联动）**：Genos 用 32 kb 窗口从 DNA 序列预测单碱基 RNA-seq 谱（log1p Pearson 0.93）。我们可在基因组规模上微调该范式：输入含目标基因启动子/编码区的 DNA 窗口（含/不含 gRNA 编辑位点），预测编辑后的表达谱变化，作为 gRNA 效率与靶点选择的"in silico 预实验"。
3. **负样本/背景序列工程（CPT 不过滤策略）**：Genos 在继续预训练阶段刻意保留基因间区、SD、转座子等"负背景"序列，让模型学到全局基因组景观。对应我们的 gRNA 效率/脱靶模型：训练集中应包含足够多"看似可用但不活跃"的 gRNA（如含 PAM 但不切割的位点、重复区域 gRNA），防止模型只学会区分正负样本的组成差异而非真实活性信号。
4. **渐进式上下文训练 + RoPE 大基频（50M）**：若我们要建模长上下文（如 CRISPR 靶点上下游 10 kb 调控环境、多基因操纵子），可采用"短窗预训练 → 逐步加长 → LR 衰减防遗忘"的三件套策略，避免直接长序列训练不稳定。
5. **MoE + 负载均衡 + Z-loss + FP32 关键运算的稳定性清单（B1）**：虽然我们的模型远小于 Genos，但"专家负载均衡 aux loss、Z-loss、Softmax/梯度累积保 FP32、BF16 主体计算"是训练大规模基因模型的实用稳定性配方，可写入我们的训练配置文档。
6. **评测协议**：所有基准统一用"冻结基础模型 embedding + 简单下游头"对比（公平性），且自建了长度递增（8K→128K）的任务验证上下文收益——我们评估 gRNA 模型时也应对同一任务采用统一下游头、多长度输入，避免架构间不公平比较。

## 6. 与我们方案的冲突/差异点
- Genos 是人类基因组模型，其预训练分布（人源序列特征、CpG 岛、人调控元件）与大肠杆菌基因组（高 GC、操纵子结构、原核 RBS/启动子）差异大，直接用于细菌序列任务需先评估迁移效果；建议对比 DNABERT（人源）、Evo 系列（跨物种含细菌）与本项目数据微调效果。
- 1 Mb 上下文、256 GPU、2,200B tokens 的训练成本远超竞赛项目承受范围——只能复用其预训练权重做下游微调，不能复现其预训练。
- RNA-seq 预测基于人类 GTEx/ENCODE 数据与 hg38；细菌场景需自建"DNA→表达"配对数据（如 E. coli 多条件转录组），不能直接套用其 checkpoint。

## 7. 行动项建议
- 将 Genos 权重（1.2B 版即可，激活 0.33B 推理成本低）纳入 M4 候选基础模型，与 DNABERT/Evo 一起做细菌下游任务（gRNA 效率、启动子强度预测）的对比微调实验。
- 复刻"冻结 DNA 编码器 + LoRA 微调文本 LLM"架构，构建"基因序列/通路描述 → 改造建议"的 LLM-Agent 原型（M4）。
- 采纳其数据工程清单（多来源整合、QC 管线、负背景序列、渐进式上下文、稳定性训练技巧）写入 README 的模型训练规范。
- 关注其后续多组学（蛋白组/代谢组）融合进展，代谢组融合方向与我们的细胞工厂表型预测直接相关。
