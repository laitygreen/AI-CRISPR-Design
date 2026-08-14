# -*- coding: utf-8 -*-
"""M1: gRNA on-target efficiency prediction.

CRISPRon-style multi-scale CNN on one-hot 30mer input.
- train(data_csv, out_dir): train regression model
- predict(seqs, model_path): predict efficiency scores
- evaluate(y_true, y_pred): Pearson/Spearman/MAE metrics
Reference: RouteA method package, DeepCRISPR (2018), CRISPRon (2021).

CLI:
    python -m aicrispr.grna_efficiency --train data.csv --out out/
    python -m aicrispr.grna_efficiency --predict 30mers.fa --model out/model.pt
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

# ---- version guard: py313 deprecated ----
if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] Python 3.13 已弃用，请使用 Python 3.10")


def onehot(seqs, L=30):
    """Encode list of sequences to (N, 4, L) one-hot tensor."""
    b2i = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    X = np.zeros((len(seqs), 4, L), dtype=np.float32)
    for i, s in enumerate(seqs):
        for j, b in enumerate(s[:L].upper()):
            if b in b2i:
                X[i, b2i[b], j] = 1.0
    return X


class GrnaEfficiencyNet(nn.Module):
    """Multi-scale CNN (kernel 3/5/7) regression head."""

    def __init__(self, n_scale=3, hidden=128):
        super().__init__()
        self.convs = nn.ModuleList([
            nn.Conv1d(4, 32, kernel_size=k, padding=k // 2)
            for k in (3, 5, 7)
        ][:n_scale])
        self.pool = nn.AdaptiveAvgPool1d(8)
        self.fc = nn.Sequential(
            nn.Linear(32 * n_scale * 8, hidden), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(hidden, 1),
        )

    def forward(self, x):
        outs = [self.pool(torch.relu(c(x))).flatten(1) for c in self.convs]
        return self.fc(torch.cat(outs, 1)).squeeze(-1)


def train(seqs, y, out_dir, epochs=80, lr=1e-3, seed=42):
    """Train efficiency model. y: array of efficiency scores (0-1)."""
    if not TORCH_OK:
        raise RuntimeError("torch 未安装")
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    X = onehot(seqs)
    n = len(seqs)
    idx = rng.permutation(n)
    ntr = int(n * 0.8)
    Xtr, Xte = X[idx[:ntr]], X[idx[ntr:]]
    ytr, yte = np.asarray(y)[idx[:ntr]], np.asarray(y)[idx[ntr:]]

    model = GrnaEfficiencyNet()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    lossf = nn.MSELoss()
    Xt = torch.tensor(Xtr)
    yt = torch.tensor(ytr, dtype=torch.float32)

    for ep in range(epochs):
        model.train()
        opt.zero_grad()
        loss = lossf(model(Xt), yt)
        loss.backward()
        opt.step()

    model.eval()
    with torch.no_grad():
        pred_tr = model(torch.tensor(Xtr)).numpy()
        pred_te = model(torch.tensor(Xte)).numpy()

    os.makedirs(out_dir, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(out_dir, "model.pt"))

    metrics = {
        "train_pearson": float(np.corrcoef(pred_tr, ytr)[0, 1]),
        "test_pearson": float(np.corrcoef(pred_te, yte)[0, 1]),
        "test_mae": float(np.mean(np.abs(pred_te - yte))),
    }
    return model, metrics


def predict(seqs, model_path):
    """Predict efficiency scores for sequences using a trained model."""
    if not TORCH_OK:
        raise RuntimeError("torch 未安装")
    model = GrnaEfficiencyNet()
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    X = torch.tensor(onehot(seqs))
    with torch.no_grad():
        return model(X).numpy()


def evaluate(y_true, y_pred):
    """Pearson / Spearman / MAE metrics."""
    yt = np.asarray(y_true, dtype=float)
    yp = np.asarray(y_pred, dtype=float)
    pearson = float(np.corrcoef(yt, yp)[0, 1])
    n = len(yt)
    rs = np.argsort(np.argsort(yt)), np.argsort(np.argsort(yp))
    d = sum((a - b) ** 2 for a, b in zip(*rs))
    spearman = 1 - 6 * d / (n * (n * n - 1)) if n > 1 else 0.0
    return {"pearson": pearson, "spearman": float(spearman),
            "mae": float(np.mean(np.abs(yt - yp)))}


def read_fasta(path):
    """Read FASTA -> (ids, seqs)."""
    ids, seqs = [], []
    cur, cur_seq = None, []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if cur:
                    seqs.append("".join(cur_seq)); ids.append(cur)
                cur = line[1:]; cur_seq = []
            elif line:
                cur_seq.append(line)
        if cur:
            seqs.append("".join(cur_seq)); ids.append(cur)
    return ids, seqs


def main():
    ap = argparse.ArgumentParser(description="gRNA efficiency (M1)")
    ap.add_argument("--train", help="CSV with columns: seq,efficiency")
    ap.add_argument("--predict", help="FASTA of 30mers")
    ap.add_argument("--model", default="out/model.pt")
    ap.add_argument("--out", default="out_routea")
    args = ap.parse_args()

    if args.train:
        import csv
        seqs, y = [], []
        with open(args.train, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                seqs.append(row["seq"]); y.append(float(row["efficiency"]))
        model, metrics = train(seqs, y, args.out)
        print("[M1 train] metrics:", metrics)
    elif args.predict:
        _, seqs = read_fasta(args.predict)
        scores = predict(seqs, args.model)
        for s, sc in zip(seqs, scores):
            print("%s\t%.3f" % (s, sc))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
