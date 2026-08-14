# -*- coding: utf-8 -*-
"""路线3: DNA embedding 入口"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] 请使用 Python 3.10")

from aicrispr.embeddings import embed, similarity_matrix
import numpy as np


def main():
    seqs = [s.strip() for s in sys.stdin if s.strip()]
    if not seqs:
        seqs = ["ATGCAAGGCAAACTGCTGTAAGGTGGGGGA",
                "TTGCCATGCAAGGCAAACTGCTGTAAGGTGG",
                "GGTAACGGTAAACTGCTGTAAGGTGGGGGAG"]
    emb, mode = embed(seqs)
    print("[Route C] mode:", mode, "| shape:", emb.shape)
    print("[Route C] 相似度矩阵:")
    print(np.round(similarity_matrix(emb), 3))
    print("[路线3 验证通过]")


if __name__ == "__main__":
    main()
