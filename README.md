# CRT Model - 30天贷款违约预测模型

基于 Freddie Mac CRT (Credit Risk Transfer) 数据的30天贷款违约预测模型，使用 GAM (Generalized Additive Model) 进行建模。

## 📊 项目概述

本项目旨在预测贷款在未来30天内是否会发生违约，使用历史贷款数据（2013-2025）进行训练和评估。

### 核心特性

- ✅ **数据源**: Supabase 云数据库（40,000条样本，平衡数据集）
- ✅ **模型**: LogisticGAM（可解释性强）
- ✅ **评估方法**: 回测、时间序列外推、交叉验证
- ✅ **性能**: AUC ~0.74-0.78, F1 ~0.69-0.71

## 🚀 快速开始

### 1. 环境要求

- Python 3.9+
- Jupyter Notebook

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行模型

```bash
cd notebooks
jupyter notebook model_training.ipynb
```

在 Jupyter 中打开后，点击 `Kernel → Restart & Run All` 运行所有代码。

## 📁 项目结构

```
CRT_Model/
├── README.md                    # 项目说明
├── requirements.txt             # Python 依赖
├── .gitignore                   # Git 忽略规则
│
├── src/                         # 核心代码模块
│   ├── config.py                # 配置管理
│   ├── data/                    # 数据加载和预处理
│   ├── features/                # 特征工程
│   ├── models/                  # 模型定义
│   ├── evaluation/              # 模型评估
│   └── utils/                   # 工具函数
│
├── notebooks/                   # Jupyter Notebooks
│   ├── model_training.ipynb     # 主要训练 Notebook
│   └── *.csv                    # 数据缓存文件
│
├── scripts/                     # 工具脚本
│   ├── check_packages.py        # 环境检查
│   └── run_tests.sh             # 测试脚本
│
├── sql_scripts/                 # SQL 脚本
│   ├── 30 Days Delinquency...   # 数据表创建
│   └── Supabase 2013-2022...    # 原始数据表定义
│
├── archived/                    # 归档文件
│   └── ...                      # 旧版本文件
│
└── docs/                        # 文档
    └── REFACTORING_SUMMARY.txt  # 重构说明
```

## 🔧 主要功能

### 数据处理

- **数据源**: 从 Supabase 获取 Freddie Mac CRT 数据
- **数据量**: 40,000 条记录（20,000 正样本 + 20,000 负样本）
- **时间范围**: 2013-2025
- **缓存机制**: 首次运行从 API 下载，后续运行直接读取 CSV

### 特征工程

- 时间特征提取（年、月）
- 利率差异计算
- 高 DTI 标记
- 近期违约标记
- 地区违约率
- 分桶特征（LTV、信用分数等）

### 模型训练

- **算法**: LogisticGAM (Generalized Additive Model)
- **优点**: 可解释性强，非线性拟合能力好
- **校准**: Isotonic Regression 概率校准
- **类别平衡**: 使用类别权重处理不平衡数据

### 模型评估

1. **回测 (Backtesting)**: 
   - 训练集: 2013-2022
   - 测试集: 2013-2022（时间顺序划分）
   - AUC: ~0.78, F1: ~0.69

2. **时间序列外推 (Time-series Out-of-Sample)**:
   - 训练集: 2013-2022
   - 测试集: 2023-2025
   - AUC: ~0.74, F1: ~0.71

3. **交叉验证 (5-Fold Stratified CV)**:
   - 数据: 2013-2022
   - AUC: 0.73 ± 0.01
   - F1: 0.71 ± 0.00

## 📊 性能指标

| 评估方法 | AUC | F1 Score | 数据集 |
|---------|-----|----------|--------|
| 回测 | 0.7783 | 0.6879 | 2013-2022 |
| 时间序列外推 | 0.7423 | 0.7112 | 2023-2025 |
| 5折交叉验证 | 0.7342±0.0071 | 0.7062±0.0034 | 2013-2022 |

## 🛠️ 技术栈

- **数据处理**: pandas, numpy
- **机器学习**: scikit-learn, pygam
- **数据库**: Supabase (PostgreSQL)
- **可视化**: matplotlib
- **开发环境**: Jupyter Notebook

## 📝 使用说明

### Cell 0: 数据下载

首次运行时，Cell 0 会从 Supabase 下载数据并保存为 CSV：

```python
# 从 Supabase 下载 40,000 条数据
# 保存为: freddie_mac_delinquency_balanced.csv
# 保存为: freddie_mac_delinquency_strict_predict_ready_GAM.csv
```

后续运行时，直接读取 CSV 文件，无需重新下载。

### Cell 1-3: 数据预处理

- 提取时间特征
- 清洗数据
- 特征选择

### Cell 4-6: 模型训练与评估

- Cell 4: 回测评估
- Cell 5: 时间序列外推评估
- Cell 6: 交叉验证评估

## 🔐 配置说明

### Supabase 连接

数据库连接信息在 `notebooks/model_training.ipynb` 的 Cell 0 中：

```python
url = "https://ptukzshzuloxipzwycte.supabase.co"
key = "your_api_key_here"
```

**注意**: 生产环境建议使用环境变量管理 API Key。

## 📈 模型可解释性

GAM 模型提供了良好的可解释性：

- **Partial Dependence Plots**: 展示每个特征对预测的影响
- **Feature Importance**: 通过 GAM 系数了解特征重要性
- **平滑曲线**: 可视化特征与目标变量的非线性关系

## 🚧 未来改进

- [ ] 添加更多特征工程
- [ ] 尝试其他模型（XGBoost、LightGBM）
- [ ] 实现模型持久化和部署
- [ ] 添加实时预测 API
- [ ] 完善文档和测试

## 📄 许可证

本项目仅供学习和研究使用。

## 👥 贡献

欢迎提出问题和建议！

## 📞 联系方式

如有问题，请通过 GitHub Issues 联系。

---

**最后更新**: 2024-11-21

