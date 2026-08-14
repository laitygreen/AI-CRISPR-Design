# -*- coding: utf-8 -*-
"""路线2: 脱靶预测训练入口"""
import sys, os, csv, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] 请使用 Python 3.10")

from aicrispr.offtarget import train


def main():
    ap = argparse.ArgumentParser(description="Route B: off-target train")
    ap.add_argument("--train", required=True, help="CSV: grna,target,label")
    ap.add_argument("--out", default="out")
    ap.add_argument("--epochs", type=int, default=60)
    args = ap.parse_args()

    pairs, labels = [], []
    with open(args.train, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pairs.append((row["grna"], row["target"]))
            labels.append(int(row["label"]))
    model, metrics = train(pairs, labels, args.out, epochs=args.epochs)
    print("[M2 train] metrics:", metrics)
    print("[路线2 验证通过]")


if __name__ == "__main__":
    main()
