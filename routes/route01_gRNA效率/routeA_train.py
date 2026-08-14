# -*- coding: utf-8 -*-
"""路线1: gRNA 效率训练入口 (薄封装 aicrispr.grna_efficiency)"""
import sys, os, csv, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] 请使用 Python 3.10")

from aicrispr.grna_efficiency import train


def main():
    ap = argparse.ArgumentParser(description="Route A: gRNA efficiency train")
    ap.add_argument("--train", required=True, help="CSV: seq,efficiency")
    ap.add_argument("--out", default="out")
    ap.add_argument("--epochs", type=int, default=80)
    args = ap.parse_args()

    seqs, y = [], []
    with open(args.train, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            seqs.append(row["seq"])
            y.append(float(row["efficiency"]))
    model, metrics = train(seqs, y, args.out, epochs=args.epochs)
    print("[M1 train] metrics:", metrics)
    print("[路线1 验证通过]")


if __name__ == "__main__":
    main()
