# -*- coding: utf-8 -*-
"""B1: Whole-genome CRISPR target scan.

Enumerate candidate gRNA (20nt + NGG PAM) across a genome FASTA, compute basic
features (GC content, poly-T, position), and export candidates table.
Reference: RouteB/A method packages; CRISPOR (2016); DeepCRISPR encoding (2018).

CLI:
    python -m aicrispr.crispr_scan --genome genome.fa --out candidates.csv
"""
import os
import sys
import csv
import argparse
import re

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] Python 3.13 已弃用，请使用 Python 3.10")

# NGG PAM 扫描窗口（与 CRISPRon 一致）：4 上游 + 20 spacer + 1 + GG + 3 下游 = 30nt
PRE_GUIDE = 4
GUIDE = 20
PRE_PAM = 1
PAM = "GG"
PAM_OFFSET = PRE_GUIDE + GUIDE + PRE_PAM  # =25，PAM 位于 30mer 索引 25-26


def scan_genome(seq, chrom="chr", min_gc=0.2, max_polyT=4):
    """Enumerate gRNA candidates with NGG PAM on forward strand."""
    candidates = []
    for i in range(len(seq) - 29):
        window = seq[i:i + 30]
        if window[PAM_OFFSET:PAM_OFFSET + 2].upper() != PAM:
            continue
        spacer = window[PRE_GUIDE:PRE_GUIDE + GUIDE]
        gc = sum(1 for b in spacer if b in "GC") / GUIDE
        polyT = max((len(m.group(0)) for m in re.finditer(r"T+", spacer)), default=0)
        if gc < min_gc or polyT > max_polyT:
            continue
        candidates.append({
            "chrom": chrom, "pos": i + 1, "strand": "+",
            "spacer": spacer, "pam": window[PAM_OFFSET:PAM_OFFSET + 2],
            "gc": round(gc, 3), "polyT": polyT,
            "context_30mer": window,
        })
    return candidates
