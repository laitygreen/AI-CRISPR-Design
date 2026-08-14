# -*- coding: utf-8 -*-
"""DNA sequence embedding extraction (DNABERT-2 preferred, local k-mer fallback).

- embed_dnabert2(seqs, model_name): HuggingFace DNABERT-2, mean pooling
- embed_kmer(seqs, k): local k-mer histogram + random projection
Reference: RouteC method package; DNABERT-2 (2024); foundation benchmark (2025).
"""
import os
import sys
import numpy as np

import os as _os
if _os.environ.get('AICRISPR_DNABERT2') == '1':
    _os.environ['TRANSFORMERS_OFFLINE'] = '1'  # 网络不可用时跳过 HF 下载
if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] Python 3.13 已弃用，请使用 Python 3.10")


def embed_kmer(seqs, k=3, dim=16):
    """k-mer histogram + fixed random projection -> (N, dim)."""
    b2i = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    n_kmers = 4 ** k
    X = np.zeros((len(seqs), n_kmers), dtype=np.float32)
    for i, s in enumerate(seqs):
        for j in range(len(s) - k + 1):
            kmer = s[j:j + k].upper()
            idx = 0
            ok = True
            for b in kmer:
                if b in b2i:
                    idx = idx * 4 + b2i[b]
                else:
                    ok = False
                    break
            if ok:
                X[i, idx] += 1.0
    X = X / (X.sum(axis=1, keepdims=True) + 1e-8)
    rng = np.random.default_rng(0)
    W = rng.normal(0, 0.1, (n_kmers, dim)).astype(np.float32)
    return X @ W


def embed_dnabert2(seqs, model_name="zhihan1996/DNABERT-2-117M"):
    """DNABERT-2 embeddings via transformers (mean pooling). Returns None on failure."""
    try:
        import torch
        from transformers import AutoModel, AutoTokenizer
    except ImportError:
        return None
    try:
        tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
    except Exception:
        return None
    model.eval()
    embs = []
    with torch.no_grad():
        for s in seqs:
            inputs = tok(s, return_tensors="pt")
            out = model(**inputs)
            embs.append(out.last_hidden_state.mean(dim=1).squeeze().numpy())
    return np.array(embs)


def embed(seqs, prefer="dnabert2", k=3, dim=16):
    """Auto: try DNABERT-2, fall back to k-mer."""
    if prefer == "dnabert2":
        emb = embed_dnabert2(seqs)
        if emb is not None:
            return emb, "dnabert2"
    return embed_kmer(seqs, k=k, dim=dim), "kmer"


def similarity_matrix(embs):
    """Cosine similarity matrix."""
    e = embs / (np.linalg.norm(embs, axis=1, keepdims=True) + 1e-8)
    return e @ e.T


if __name__ == "__main__":
    import sys
    seqs = [s.strip() for s in sys.stdin if s.strip()]
    if not seqs:
        seqs = ["ATGCAAGGCAAACTGCTGTAAGGTGGGGGA",
                "TTGCCATGCAAGGCAAACTGCTGTAAGGTGG",
                "GGTAACGGTAAACTGCTGTAAGGTGGGGGAG"]
    emb, mode = embed(seqs)
    print("mode:", mode, "| shape:", emb.shape)
    print("similarity matrix:")
    print(np.round(similarity_matrix(emb), 3))
