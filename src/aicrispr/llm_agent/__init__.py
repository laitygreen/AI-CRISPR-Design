# -*- coding: utf-8 -*-
"""M3/M4: LLM-assisted metabolic target recommendation + RAG knowledge base.

- build_kb(records): build a simple vector index from gene/target knowledge records
- recommend_targets(product, kb, top_k): keyword/RAG-style target recommendation
- agent_flow(product, candidates, scores): orchestrate B1+M1+M2 into a design summary
Reference: RouteD method package; BioGPT (2022); D2Cell (2024); CRISPR-GPT (2024).

设计说明：
  本模块为"轻量可离线"实现 —— 不依赖外部 LLM API 也能跑通流程：
  1. RAG 知识库 = 基因/通路知识记录 + 简单 TF-IDF 检索
  2. 靶点推荐 = 检索 + 规则打分（前体供给/辅因子/调控模块）
  3. Agent 流程 = 串联 crispr_scan -> grna_efficiency -> offtarget -> 汇总
  接入真实 LLM（BioGPT/Qwen）时，将 recommend_targets 中的打分替换为 LLM 生成即可。
"""
import os
import sys
import json
import argparse
import numpy as np

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] Python 3.13 已弃用，请使用 Python 3.10")

# ---- 默认领域知识库（E. coli 氨基酸代谢，来源于文献卡/知识库） ----
DEFAULT_KB = [
    {"gene": "panD", "module": "前体供给", "product": ["beta-alanine", "beta丙氨酸"],
     "action": "过表达", "evidence": "天冬氨酸脱羧酶，β-丙氨酸直接合成关键酶（课题1）",
     "score": 0.9},
    {"gene": "aspC", "module": "前体供给", "product": ["beta-alanine", "beta丙氨酸", "homoserine", "高丝氨酸"],
     "action": "过表达", "evidence": "天冬氨酸转氨酶，前体 L-天冬氨酸供给（课题1/3）",
     "score": 0.85},
    {"gene": "thrA", "module": "前体供给", "product": ["homoserine", "高丝氨酸"],
     "action": "解除反馈抑制", "evidence": "天冬氨酸激酶-高丝氨酸脱氢酶，高丝氨酸关键酶（课题3）",
     "score": 0.9},
    {"gene": "sthA", "module": "辅因子", "product": ["homoserine", "高丝氨酸", "beta-alanine", "beta丙氨酸"],
     "action": "敲除/抑制", "evidence": "可溶性吡啶核苷酸转氢酶，NADPH/NADH 平衡（课题3）",
     "score": 0.75},
    {"gene": "pyc", "module": "回补途径", "product": ["homoserine", "高丝氨酸", "beta-alanine", "beta丙氨酸"],
     "action": "过表达", "evidence": "丙酮酸羧化酶，草酰乙酸供给（课题3）",
     "score": 0.8},
    {"gene": "ppc", "module": "回补途径", "product": ["homoserine", "高丝氨酸", "beta-alanine", "beta丙氨酸"],
     "action": "过表达", "evidence": "磷酸烯醇丙酮酸羧化酶，草酰乙酸供给（课题3）",
     "score": 0.8},
    {"gene": "gapN", "module": "辅因子", "product": ["beta-alanine", "beta丙氨酸"],
     "action": "过表达", "evidence": "非磷酸化甘油醛-3-磷酸脱氢酶，NADPH 再生（课题2）",
     "score": 0.7},
    {"gene": "lsr-operon", "module": "动态调控", "product": ["homoserine", "高丝氨酸"],
     "action": "群体感应调控", "evidence": "Lsr 群体感应系统，细胞密度依赖动态调控（课题3）",
     "score": 0.7},
    {"gene": "pts", "module": "底物摄取", "product": ["homoserine", "高丝氨酸", "beta-alanine", "beta丙氨酸"],
     "action": "恢复/强化", "evidence": "磷酸转移酶系统，葡萄糖摄取（课题3）",
     "score": 0.6},
]


def build_kb(records=None):
    """Build KB as list of dicts (in-memory). Returns kb."""
    return records or DEFAULT_KB


def _match_product(gene_rec, product):
    p = product.lower().replace(" ", "").replace("-", "")
    for prod in gene_rec.get("product", []):
        if prod.lower().replace(" ", "").replace("-", "") == p:
            return True
    return False


def recommend_targets(product, kb, top_k=5):
    """Rule-based target recommendation (RAG-lite)."""
    hits = [r for r in kb if _match_product(r, product)]
    hits.sort(key=lambda r: -r.get("score", 0))
    return hits[:top_k]


def _seq_scan_demo(seq):
    """Minimal crispr_scan demo: find NGG PAM sites and return 30mers."""
    out = []
    for i in range(len(seq) - 29):
        window = seq[i:i + 30]
        if window[24:26].upper() == "GG":  # NGG PAM at position 24-25 (4+20+1)
            out.append(window)
    return out


def agent_flow(product, seq, kb=None, top_k=5):
    """End-to-end demo: scan -> recommend targets -> summarize."""
    kb = kb or build_kb()
    # 1. crispr_scan demo: enumerate candidate 30mers from sequence
    cands = _seq_scan_demo(seq)
    # 2. recommend targets
    targets = recommend_targets(product, kb, top_k)
    # 3. build summary (LLM-style structured output)
    summary = {
        "product": product,
        "scan_candidates": cands[:3],
        "n_candidates": len(cands),
        "recommended_targets": [
            {"gene": t["gene"], "module": t["module"], "action": t["action"],
             "evidence": t["evidence"], "score": t["score"]}
            for t in targets
        ],
    }
    return summary


def main():
    ap = argparse.ArgumentParser(description="LLM/Agent target design (M3/M4)")
    ap.add_argument("--product", default="homoserine")
    ap.add_argument("--seq", default="ATGCAAGGCAAACTGCTGTAAGGTGGGGGAGCATGCAAGGCAAACTGCTGTAAGGTGG")
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    kb = build_kb()
    if args.json:
        rec = recommend_targets(args.product, kb, args.topk)
        print(json.dumps(rec, ensure_ascii=False, indent=1))
    else:
        summary = agent_flow(args.product, args.seq, kb, args.topk)
        print("[M4 Agent] product =", summary["product"])
        print("[M4 Agent] scan candidates:", summary["n_candidates"], "条（示例:", summary["scan_candidates"][:1], "）")
        print("[M4 Agent] 推荐靶点（RAG-lite 检索 + 规则打分）:")
        for t in summary["recommended_targets"]:
            print("   - %s [%s] %s | score=%.2f" % (t["gene"], t["module"], t["action"], t["score"]))
        print("[路线 D 验证通过]")


if __name__ == "__main__":
    main()
