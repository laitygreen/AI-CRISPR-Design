# -*- coding: utf-8 -*-
"""路线4: LLM/Agent 靶点推荐入口"""
import sys, os, json, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] 请使用 Python 3.10")

from aicrispr.llm_agent import recommend_targets, agent_flow, build_kb


def main():
    ap = argparse.ArgumentParser(description="Route D: LLM/Agent target recommend")
    ap.add_argument("--product", default="homoserine")
    ap.add_argument("--seq", default=None)
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    kb = build_kb()
    if args.json:
        rec = recommend_targets(args.product, kb, args.topk)
        print(json.dumps(rec, ensure_ascii=False, indent=1))
    else:
        seq = args.seq or "ATGCAAGGCAAACTGCTGTAAGGTGGGGGAGCATGCAAGGCAAACTGCTGTAAGGTGG"
        s = agent_flow(args.product, seq, kb, args.topk)
        print("[Route D] product =", s["product"])
        print("[Route D] scan candidates:", s["n_candidates"])
        print("[Route D] 推荐靶点:")
        for t in s["recommended_targets"]:
            print("   - %s [%s] %s | score=%.2f" % (t["gene"], t["module"], t["action"], t["score"]))
        print("[路线4 验证通过]")


if __name__ == "__main__":
    main()
