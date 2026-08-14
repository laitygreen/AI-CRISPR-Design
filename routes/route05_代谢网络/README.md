# 路线 5：代谢网络建模（Route E / B2）

## 功能
用 cobrapy + iML1515 进行基因组规模代谢建模（FBA/pFBA/FVA），识别 β-丙氨酸 / L-高丝氨酸合成瓶颈。

- FBA：目标函数优化 + shadow price 瓶颈分析
- pFBA：最小通量最优解 + 高通量反应排序
- 模型：iML1515（E. coli K-12 MG1655，1516 基因 / 2712 反应）

## 快速开始（Python 3.10）

```bash
# FBA 分析
python routeE_fba.py --fba

# 瓶颈识别
python routeE_fba.py --bottlenecks --product EX_ala_B_e

# 本地模型文件（避免在线加载）
python routeE_fba.py --fba --model iML1515.json
```

## iML1515 获取
- 在线：cobra 自动从 BiGG 下载（网络要求）
- 离线：下载 iML1515.json 后用 --model 指定
  - BiGG: https://bigg.ucsd.edu/models/iML1515
  - GitHub: SBRG/bigg_models

## 依赖
cobra（pip install cobra） / numpy（Python 3.10）

## 文献支撑
- iML1515 (Monk 2017) Nat Biotechnol
- Lewis 2010 Mol Syst Biol（进化菌株多组学验证）
- 详见 docs/methods/RouteE_代谢网络与多组学方法包.md
