# -*- coding: utf-8 -*-
"""路线1: gRNA 效率推理入口"""
import sys, os, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] 请使用 Python 3.10")

from aicrispr.grna_efficiency import predict, read_fasta


def main():
    ap = argparse.ArgumentParser(description="Route A: gRNA efficiency predict")
    ap.add_argument("--predict", required=True, help="FASTA of 30mers")
    ap.add_argument("--model", required=True, help="trained model.pt")
    args = ap.parse_args()

    _, seqs = read_fasta(args.predict)
    scores = predict(seqs, args.model)
    for s, sc in zip(seqs, scores):
        print("%s\t%.3f" % (s, sc))


if __name__ == "__main__":
    main()
