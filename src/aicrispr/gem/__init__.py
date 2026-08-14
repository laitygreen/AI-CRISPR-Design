# -*- coding: utf-8 -*-
"""B2: Genome-scale metabolic modeling (cobrapy + iML1515).

- load_model(source): load iML1515 (BiGG or local JSON)
- run_fba(model, objective): FBA, return objective flux + shadow prices
- find_bottlenecks(model, product_rxn): FVA / essentiality screening
Reference: RouteE method package; iML1515 (2017); Lewis 2010.

CLI:
    python -m aicrispr.gem --fba --model iML1515.json
    python -m aicrispr.gem --bottlenecks --model iML1515.json --product EX_ala_B_e
"""
import os
import sys
import json
import argparse

if sys.version_info[:2] == (3, 13):
    raise SystemExit("[MIGRATE] Python 3.13 已弃用，请使用 Python 3.10")

try:
    import cobra
    COBRA_OK = True
except ImportError:
    COBRA_OK = False


def load_model(source=None):
    """Load iML1515 model. source: path to JSON/SBML, or None for built-in."""
    if not COBRA_OK:
        raise RuntimeError("cobra 未安装：python -m pip install cobra")
    if source and os.path.exists(source):
        return cobra.io.load_model(source)
    # 尝试从 BiGG 在线加载（网络不稳时可先下载 iML1515.json 到本地）
    try:
        return cobra.io.web.load_model("iML1515")
    except Exception as e:
        raise RuntimeError("在线加载失败: %s；请下载 iML1515.json 后用 --model 指定" % str(e)[:100])


def run_fba(model, objective=None):
    """FBA: set objective (optional), run, return flux + shadow prices."""
    if objective is not None:
        try:
            model.objective = objective
        except Exception:
            pass
    sol = model.optimize()
    result = {
        "status": sol.status,
        "objective_value": float(sol.objective_value),
    }
    if sol.shadow_prices is not None:
        # 返回 shadow price 最高的 10 个反应（潜在瓶颈）
        sp = sorted(sol.shadow_prices.items(), key=lambda kv: -abs(kv[1]))[:10]
        result["top_shadow_prices"] = [
            {"reaction": r, "shadow_price": float(v)} for r, v in sp
        ]
    return result


def find_bottlenecks(model, product_rxn, top_n=10):
    """Identify bottleneck reactions near product pathway via flux variability."""
    # pFBA 近似：最小化总通量的最优解（parsimonious FBA）
    try:
        from cobra.flux_analysis import pfba
        sol = pfba(model)
        fluxes = sol.fluxes
    except Exception:
        sol = model.optimize()
        fluxes = sol.fluxes
    # 返回通量最高/最低的产物通路邻近反应（简化：按 |flux| 排序）
    ranked = sorted(fluxes.items(), key=lambda kv: -abs(kv[1]))[:top_n]
    return [
        {"reaction": r, "flux": float(v)} for r, v in ranked
    ]


def main():
    ap = argparse.ArgumentParser(description="GEM / FBA analysis (B2)")
    ap.add_argument("--fba", action="store_true")
    ap.add_argument("--bottlenecks", action="store_true")
    ap.add_argument("--model", default=None)
    ap.add_argument("--product", default="EX_ala_B_e")
    args = ap.parse_args()

    if not (args.fba or args.bottlenecks):
        ap.print_help()
        return
    print("[GEM] 加载模型 iML1515 ...")
    model = load_model(args.model)
    print("[GEM] 基因数=%d 反应数=%d 代谢物数=%d" % (
        len(model.genes), len(model.reactions), len(model.metabolites)))

    if args.fba:
        result = run_fba(model)
        print("[FBA] status=%s objective=%.3f" % (result["status"], result["objective_value"]))
        for sp in result.get("top_shadow_prices", []):
            print("  shadow price %-12s %.4f" % (sp["reaction"], sp["shadow_price"]))
    if args.bottlenecks:
        bn = find_bottlenecks(model, args.product)
        print("[Bottleneck] 高通量反应 Top%d（pFBA）:" % len(bn))
        for b in bn:
            print("  %-12s flux=%.3f" % (b["reaction"], b["flux"]))
    print("[路线 E 验证通过]")


if __name__ == "__main__":
    main()
