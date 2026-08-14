# -*- coding: utf-8 -*-
"""路线2: 脱靶预测推理入口"""
import sys, os, csv, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] 请使用 Python 3.10")

from aicrispr.offtarget import predict


def main():
    ap = argparse.ArgumentParser(description="Route B: off-target predict")
    ap.add_argument("--predict", required=True, help="CSV: grna,target")
    ap.add_argument("--model", required=True)
    args = ap.parse_args()

    with open(args.predict, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    grna = rows[0]["grna"]
    cands = [r["target"] for r in rows]
    scores = predict(grna, cands, args.model)
    for c, s in zip(cands, scores):
        print("%s\t%.3f" % (c, s))


if __name__ == "__main__":
    main()
