# -*- coding: utf-8 -*-
"""
五路线一键验证（AI-CRISPR-Design 包）
运行：python demo_routes.py  （用 Python 3.10）
"""
import sys
import numpy as np

print("=" * 60)
print("AI-CRISPR 五路线验证")
print("Python:", sys.version.split()[0])
print("=" * 60)

# ---- B1: crispr_scan ----
print("\n[B1] CRISPR 位点扫描 ...")
from aicrispr.crispr_scan import scan_genome
seq = "ATGCAAGGCAAACTGCTGTAAGGTGGGGGAGCATGCAAGGCAAACTGCTGTAAGGTGG"
cands = scan_genome(seq)
print("  候选 gRNA:", len(cands), "条 | 示例:", cands[0]["spacer"], cands[0]["pam"])

# ---- A: grna_efficiency ----
print("\n[A] gRNA 效率预测 (M1) ...")
from aicrispr.grna_efficiency import train, evaluate
import tempfile, os
rng = np.random.default_rng(42)
seqs = ["".join(rng.choice(list("ACGT"), size=30)) for _ in range(120)]
gc = np.array([sum(1 for b in s if b in "GC") / 30 for s in seqs])
y = np.clip(0.25 + 0.75 * gc + rng.normal(0, 0.05, 120), 0, 1)
model, metrics = train(seqs, y, tempfile.mkdtemp(), epochs=40)
print("  train_pearson=%.3f test_pearson=%.3f" % (metrics["train_pearson"], metrics.get("test_pearson", 0)))

# ---- B: offtarget ----
print("\n[B] 脱靶预测 (M2) ...")
from aicrispr.offtarget import train as ot_train

def make_pairs(n_pos=100, n_neg=150):
    rng = np.random.default_rng(7)
    pairs, labels = [], []
    for _ in range(n_pos):
        g = "".join(rng.choice(list("ACGT"), size=20))
        t = list(g)
        for _ in range(int(rng.integers(0, 3))):
            p = int(rng.integers(0, 20)); t[p] = rng.choice([b for b in "ACGT" if b != t[p]])
        pairs.append((g, "".join(t))); labels.append(1)
    for _ in range(n_neg):
        g = "".join(rng.choice(list("ACGT"), size=20))
        t = list(g)
        for _ in range(int(rng.integers(4, 9))):
            p = int(rng.integers(0, 20)); t[p] = rng.choice([b for b in "ACGT" if b != t[p]])
        pairs.append((g, "".join(t))); labels.append(0)
    return pairs, labels

pairs, labels = make_pairs()
m2, m2m = ot_train(pairs, labels, tempfile.mkdtemp(), epochs=30)
print("  AUROC=%.3f Acc=%.3f" % (m2m["auroc"], m2m["accuracy"]))

# ---- C: embeddings ----
print("\n[C] DNA embedding ...")
from aicrispr.embeddings import embed
emb, mode = embed(seqs[:3])
print("  mode:", mode, "| shape:", emb.shape)

# ---- D: llm_agent ----
print("\n[D] LLM/Agent 靶点推荐 (M3/M4) ...")
from aicrispr.llm_agent import agent_flow, build_kb
summary = agent_flow("homoserine", seq, build_kb(), 5)
print("  推荐:", ", ".join(t["gene"] for t in summary["recommended_targets"]))

# ---- E: gem (cobra) ----
print("\n[E] 代谢网络 (B2, cobra) ...")
try:
    import cobra
    from aicrispr.gem import load_model
    model = load_model()
    print("  iML1515 加载 OK: %d 基因 / %d 反应" % (len(model.genes), len(model.reactions)))
except Exception as e:
    print("  [跳过] cobra/iML1515 未就绪:", str(e)[:80])

print("\n" + "=" * 60)
print("五路线验证完成")
print("=" * 60)
