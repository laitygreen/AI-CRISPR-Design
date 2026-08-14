# AI-CRISPR Design System

AI 驱动的 CRISPR 基因编辑设计系统，面向大肠杆菌（E. coli）氨基酸细胞工厂（β-丙氨酸 / L-高丝氨酸）的代谢工程改造。

## 功能模块（五路线全实现）

| 模块 | 路径 | 功能 | 状态 |
|---|---|---|---|
| crispr_scan | src/aicrispr/crispr_scan/ | 全基因组 PAM 扫描 + gRNA 候选枚举 + 特征化（B1） | ✅ 已实现 |
| grna_efficiency | src/aicrispr/grna_efficiency/ | gRNA 编辑效率预测模型（M1，多尺度 CNN） | ✅ 已实现 |
| offtarget | src/aicrispr/offtarget/ | 脱靶风险评估模型（M2，双路 CNN+MLP） | ✅ 已实现 |
| embeddings | src/aicrispr/embeddings/ | DNA embedding 提取（DNABERT-2 / k-mer 降级） | ✅ 已实现 |
| llm_agent | src/aicrispr/llm_agent/ | LLM 辅助靶点推荐 + RAG 知识库 + Agent 流程（M3/M4） | ✅ 已实现 |
| gem | src/aicrispr/gem/ | 代谢网络建模（FBA/pFBA，cobrapy + iML1515）（B2） | ✅ 已实现 |

## 五路线验证（2026-08-14, Python 3.10）

    python demo_routes.py

| 路线 | 验证结果 |
|---|---|
| B1 扫描 | 示例序列检出 5 候选 gRNA（spacer+PAM+GC+polyT 特征） |
| A 效率 | train r=0.786 / test r=0.557（合成标签演示） |
| B 脱靶 | AUROC=0.980（合成数据） |
| C embedding | k-mer 模式（DNABERT-2 需网络） |
| D 靶点推荐 | 高丝氨酸 → thrA/aspC/pyc/ppc/sthA |
| E 代谢网络 | iML1515 加载成功（1516 基因 / 2712 反应） |

> 注：A/B 的标签为合成数据（流程验证）；接入 rth.dk / GUIDE-seq 真实数据后重训。

## 环境依赖与迁移性说明（重要）

本项目设计为跨平台可迁移，所有依赖已声明于：

- pyproject.toml — 统一依赖声明（pip 安装入口；requires-python >=3.10,<3.13）
- requirements.txt — 核心依赖锁定
- environment.yml — conda 全量环境
- requirements-tf1.txt — DeepCRISPR 旧版 TF1 环境（隔离，建议 Docker）

### 快速开始

    # Python 3.10（3.13 已弃用，脚本内置版本守卫）
    python -m pip install -e .

    # 五路线一键验证
    python demo_routes.py

    # 单模块使用
    python -c "from aicrispr.grna_efficiency import train"
    python -c "from aicrispr.offtarget import train"
    python -c "from aicrispr.llm_agent import agent_flow"

### 第三方代码（third_party/）

本仓库不复制第三方完整源码，通过 third_party/README.md 记录来源与获取方式，避免仓库膨胀与许可证冲突。

## 项目结构

    AI-CRISPR-Design/
    ├── pyproject.toml        # 依赖声明（可迁移核心）
    ├── demo_routes.py        # 五路线一键验证
    ├── src/aicrispr/         # 核心 Python 包（6 模块）
    ├── docs/                 # 方案 + 知识库 + 方法学习包
    ├── scripts/              # 一键复现脚本
    ├── notebooks/            # 分析演示
    └── tests/                # 测试
