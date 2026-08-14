# AI-CRISPR Design System

AI 驱动的 CRISPR 基因编辑设计系统，面向大肠杆菌（E. coli）氨基酸细胞工厂（β-丙氨酸 / L-高丝氨酸）的代谢工程改造。赛道二参赛项目：AI 基因编辑与核酸工具设计。

## 功能模块

| 模块 | 路径 | 功能 |
|---|---|---|
| crispr_scan | src/aicrispr/crispr_scan/ | 全基因组 PAM 扫描 + gRNA 候选枚举 + 特征化（B1） |
| grna_efficiency | src/aicrispr/grna_efficiency/ | gRNA 编辑效率预测模型（M1） |
| offtarget | src/aicrispr/offtarget/ | 脱靶风险评估模型（M2） |
| embeddings | src/aicrispr/embeddings/ | DNA 预训练模型 embedding 提取（DNABERT-2 等） |
| gem | src/aicrispr/gem/ | 代谢网络建模（FBA/pFBA，cobrapy + iML1515）（B2） |

## 环境依赖与迁移性说明（重要）

本项目设计为跨平台可迁移，所有依赖已声明于：

- pyproject.toml — 统一依赖声明（pip 安装入口）
- requirements.txt — 核心依赖锁定
- environment.yml — conda 全量环境（推荐，含 Python 3.11 锁定）
- requirements-tf1.txt — DeepCRISPR 旧版 TF1 环境（隔离，建议 Docker）

### 快速开始

    # 方式 1：conda（推荐，跨平台一致）
    conda env create -f environment.yml
    conda activate aicrispr

    # 方式 2：pip
    python -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -e .

    # 运行测试
    pytest tests/

### 平台注意

| 依赖 | Windows | Linux/macOS |
|---|---|---|
| cobrapy (FBA) | 可装（swiglpk 需编译） | 可直接安装 |
| pysam | 需预编译 wheel | 可直接安装 |
| tensorflow 1.15 (DeepCRISPR) | 仅 Docker | 仅 Docker |
| DESeq2 (R) | 需 R 环境 | 需 R 环境 |

### 第三方代码（third_party/）

本仓库不复制第三方完整源码，通过 third_party/README.md 记录来源与获取方式，避免仓库膨胀与许可证冲突。

## 项目结构

    AI-CRISPR-Design/
    ├── pyproject.toml        # 依赖声明（可迁移核心）
    ├── requirements.txt      # pip 锁定
    ├── environment.yml       # conda 全量环境
    ├── src/aicrispr/         # 核心 Python 包
    ├── scripts/              # 一键复现脚本
    ├── docs/                 # 方案 + 知识库 + 方法学习包
    ├── notebooks/            # 分析演示
    ├── tests/                # 测试
    ├── data/                 # 数据（gitignore，不含大文件）
    └── third_party/          # 第三方代码来源记录

## 文档

- 参赛方案：docs/挑战赛参赛方案_赛道二_AI-CRISPR智能设计系统_v2.md
- 知识库：docs/knowledge_base/
- 方法学习包：docs/methods/（5 路线：gRNA效率/脱靶/DNA底座/LLM/代谢网络）
- 文献库：docs/literature/（294 篇分级 + 25 篇精读卡）

## 许可

MIT License（本仓库代码）。第三方代码遵循各自许可证，见 third_party/README.md。
