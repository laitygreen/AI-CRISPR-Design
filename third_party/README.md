# Third-party Code Sources

本目录不复制第三方完整源码，仅记录来源与获取方式（避免仓库膨胀与许可证冲突）。

| 工具 | GitHub 仓库 | 用途 | 许可证 | 本地镜像 |
|---|---|---|---|---|
| DeepCRISPR | bm2-lab/DeepCRISPR | gRNA效率+脱靶（TF1） | Apache-2.0 | exp design/methods/repos/DeepCRISPR-master |
| CRISPRon | RTH-tools/crispron | gRNA效率（PyTorch） | AGPL-3.0 | exp design/methods/repos/crispron-main |
| Azimuth | MicrosoftResearch/Azimuth | Doench 2016 评分 | MIT | exp design/methods/repos/Azimuth-master |
| CRISPR-Net | JasonLinjc/CRISPR-Net | 脱靶 RCNN | 学术 | exp design/methods/repos/CRISPR-Net-master |
| DNABERT | jerryji1993/DNABERT | k-mer 底座 | Apache-2.0 | exp design/methods/repos/DNABERT-master |
| DNABERT-2 | MAGICS-LAB/DNABERT_2 | BPE 底座 | Apache-2.0 | exp design/methods/repos/DNABERT_2-main |
| Nucleotide Transformer | instadeepai/nucleotide-transformer | NT 底座 | Apache-2.0 | exp design/methods/repos/nucleotide-transformer-main |
| HyenaDNA | HazyResearch/hyena-dna | 长上下文底座 | Apache-2.0 | exp design/methods/repos/hyena-dna-main |
| cobrapy | opencobra/cobrapy | FBA 建模 | Apache-2.0 | exp design/methods/repos/cobrapy-devel |
| breseq | barricklab/breseq | ALE 变异解析 | GPL-3.0 | exp design/methods/repos/breseq-master |
| CRISPResso2 | pinellolab/CRISPResso2 | 编辑效率分析 | AGPL-3.0 | exp design/methods/repos/CRISPResso2-master |
| BioGPT | microsoft/BioGPT | LLM 底座 | MIT | 线上获取 |
| BioT5 | QizhiPei/BioT5 | LLM 底座 | 需查证 | 线上获取 |
| CRISPR-GPT | cong-lab/crispr-gpt-pub | LLM Agent | 需查证 | 线上获取 |

## 获取方式

    git clone <url>
    # 或 codeload 下载: https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/<branch>

注意：部分仓库需遵循各自许可证（AGPL/GPL 传染性），在参赛提交时确认合规。
