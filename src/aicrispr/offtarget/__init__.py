# -*- coding: utf-8 -*-
"""M2: CRISPR off-target risk prediction.

Dual-path model: mismatch vector (MLP) + sequence CNN (gRNA vs candidate).
- train(pairs_csv, out_dir)
- predict(grna, candidates, model_path)
- evaluate(y_true, y_pred): AUROC / Accuracy
Reference: RouteB method package, CRISPR-Net (2018), DNABERT-Epi (2025).

CLI:
    python -m aicrispr.offtarget --train pairs.csv --out out/
    python -m aicrispr.offtarget --predict grna.fa cand.fa --model out/model.pt
"""
import os
import sys
import argparse
import numpy as np

try:
    import torch
    import torch.nn as nn
    TORCH_OK = True
except ImportError:
    TORCH_OK = False

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] Python 3.13 已弃用，请使用 Python 3.10")


def mismatch_vector(grna, target, L=20):
    """20-dim mismatch indicator (1=mismatch)."""
    return np.array([1.0 if a.upper() != b.upper() else 0.0
                     for a, b in zip(grna[:L], target[:L])], dtype=np.float32)


def onehot_pair(grna, target, L=20):
    """(4, 2L) one-hot for gRNA + candidate."""
    b2i = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    x = np.zeros((4, 2 * L), dtype=np.float32)
    for j, s in enumerate([grna, target]):
        for i, b in enumerate(s[:L].upper()):
            if b in b2i:
                x[b2i[b], j * L + i] = 1.0
    return x


class OffTargetNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(4, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.AdaptiveAvgPool1d(5)
        self.mlp = nn.Sequential(nn.Linear(20, 32), nn.ReLU())
        self.fc = nn.Sequential(
            nn.Linear(32 * 5 + 32, 64), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(64, 1),
        )

    def forward(self, seq_x, mm_x):
        h = torch.relu(self.conv1(seq_x))
        h = torch.relu(self.conv2(h))
        h = self.pool(h).flatten(1)
        m = self.mlp(mm_x)
        return self.fc(torch.cat([h, m], 1)).squeeze(-1)


def train(pairs, labels, out_dir, epochs=60, lr=1e-3, seed=7):
    """pairs: list of (grna, target); labels: 0/1."""
    if not TORCH_OK:
        raise RuntimeError("torch 未安装")
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    mm = np.stack([mismatch_vector(g, t) for g, t in pairs], dtype=np.float32)
    Xs = np.stack([onehot_pair(g, t) for g, t in pairs], dtype=np.float32)
    y = np.asarray(labels, dtype=np.float32)

    idx = rng.permutation(len(pairs))
    ntr = int(len(pairs) * 0.8)
    tr, te = idx[:ntr], idx[ntr:]

    model = OffTargetNet()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    lossf = nn.BCEWithLogitsLoss()
    Xs_t = torch.tensor(Xs[tr]); mm_t = torch.tensor(mm[tr]); y_t = torch.tensor(y[tr])

    for ep in range(epochs):
        model.train(); opt.zero_grad()
        loss = lossf(model(Xs_t, mm_t), y_t)
        loss.backward(); opt.step()

    model.eval()
    with torch.no_grad():
        p = torch.sigmoid(model(torch.tensor(Xs[te]), torch.tensor(mm[te]))).numpy()
    yv = y[te]
    acc = float(((p > 0.5).astype(int) == yv).mean())

    order = np.argsort(p)[::-1]
    tp = np.cumsum(yv[order] == 1) / max((yv == 1).sum(), 1)
    fp = np.cumsum(yv[order] == 0) / max((yv == 0).sum(), 1)
    try:
        from scipy.integrate import trapezoid as trapz
    except ImportError:
        from numpy import trapezoid as trapz
    auroc = float(trapz(tp, fp)) if len(tp) > 1 else 0.0

    os.makedirs(out_dir, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(out_dir, "model.pt"))
    return model, {"auroc": auroc, "accuracy": acc}


def predict(grna, candidates, model_path):
    if not TORCH_OK:
        raise RuntimeError("torch 未安装")
    model = OffTargetNet()
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    mm = torch.tensor(np.stack([mismatch_vector(grna, c) for c in candidates], dtype=np.float32))
    Xs = torch.tensor(np.stack([onehot_pair(grna, c) for c in candidates], dtype=np.float32))
    with torch.no_grad():
        return torch.sigmoid(model(Xs, mm)).numpy()


def main():
    ap = argparse.ArgumentParser(description="off-target risk (M2)")
    ap.add_argument("--train", help="CSV: grna,target,label")
    ap.add_argument("--predict", help="CSV: grna,target (no label)")
    ap.add_argument("--model", default="out/model.pt")
    ap.add_argument("--out", default="out_routeb")
    args = ap.parse_args()

    if args.train:
        import csv
        pairs, labels = [], []
        with open(args.train, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                pairs.append((row["grna"], row["target"]))
                labels.append(int(row["label"]))
        model, metrics = train(pairs, labels, args.out)
        print("[M2 train] metrics:", metrics)
    elif args.predict:
        import csv
        with open(args.predict, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        grna = rows[0]["grna"]
        cands = [r["target"] for r in rows]
        scores = predict(grna, cands, args.model)
        for c, s in zip(cands, scores):
            print("%s\t%.3f" % (c, s))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
