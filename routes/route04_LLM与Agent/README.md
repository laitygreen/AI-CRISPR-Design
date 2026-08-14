# 路线 4：LLM/Agent 靶点设计（Route D / M3+M4）

## 功能
给定目标产物（β-丙氨酸 / L-高丝氨酸），推荐代谢工程靶点组合与编辑策略。

- RAG-lite 知识库：基因/通路/产物知识记录 + 规则打分检索
- Agent 流程：crispr_scan → 靶点推荐 → 结构化汇总
- 可扩展：将规则打分替换为 LLM 生成（BioGPT/Qwen）

## 快速开始（Python 3.10）

```bash
# 靶点推荐（JSON 输出）
python routeD_recommend.py --product homoserine --json

# 端到端 Agent 流程
python routeD_recommend.py --product beta丙氨酸 --seq "ATGCAAGGCAAACTG..."

# 包 API
python -c "from aicrispr.llm_agent import agent_flow, build_kb; s=agent_flow('homoserine', 'A'*60, build_kb()); print([t['gene'] for t in s['recommended_targets']])"
```

## 内置知识库示例
| 基因 | 模块 | 产物 | 动作 |
|---|---|---|---|
| thrA | 前体供给 | 高丝氨酸 | 解除反馈抑制 |
| aspC | 前体供给 | β-丙氨酸/高丝氨酸 | 过表达 |
| pyc/ppc | 回补途径 | 草酰乙酸供给 | 过表达 |
| sthA | 辅因子 | NADPH/NADH 平衡 | 敲除 |
| gapN | 辅因子 | NADPH 再生 | 过表达 |
| lsr-operon | 动态调控 | 群体感应 | 调控 |

## 依赖
numpy / json（纯标准库 + numpy，无需 LLM API 即可运行）

## 文献支撑
- BioGPT (2022) Brief Bioinform
- D2Cell / LLM for Metabolic Engineering (2024) bioRxiv
- CRISPR-GPT (2024) bioRxiv
- 详见 docs/methods/RouteD_LLM与Agent方法包.md
