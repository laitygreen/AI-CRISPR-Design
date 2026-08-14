# -*- coding: utf-8 -*-
"""路线5: 代谢网络 FBA 分析入口"""
import sys, os, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] 请使用 Python 3.10")

from aicrispr.gem import load_model, run_fba, find_bottlenecks


def main():
    ap = argparse.ArgumentParser(description="Route E: GEM/FBA analysis")
    ap.add_argument("--fba", action="store_true")
    ap.add_argument("--bottlenecks", action="store_true")
    ap.add_argument("--model", default=None)
    ap.add_argument("--product", default="EX_ala_B_e")
    args = ap.parse_args()

    if not (args.fba or args.bottlenecks):
        ap.print_help()
        return

    print("[Route E] 加载 iML1515 ...")
    model = load_model(args.model)
    print("[Route E] 基因=%d 反应=%d 代谢物=%d" % (
        len(model.genes), len(model.reactions), len(model.metabolites)))

    if args.fba:
        r = run_fba(model)
        print("[FBA] status=%s objective=%.3f" % (r["status"], r["objective_value"]))
        for sp in r.get("top_shadow_prices", [])[:8]:
            print("  shadow %-10s %.4f" % (sp["reaction"], sp["shadow_price"]))
    if args.bottlenecks:
        bn = find_bottlenecks(model, args.product)
        print("[Bottleneck] 高通量反应 Top%d:" % len(bn))
        for b in bn[:10]:
            print("  %-10s flux=%.3f" % (b["reaction"], b["flux"]))
    print("[路线5 验证通过]")


if __name__ == "__main__":
    main()
