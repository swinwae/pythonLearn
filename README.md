# Python 学习示例 / Python Learning Examples

本仓库包含一系列由浅入深的 Python 学习示例，适合初学者系统学习 Python 核心概念。

## 文件列表

| 文件 | 主题 | 核心内容 |
|------|------|----------|
| `01_basics.py` | 基础语法 | 变量、数据类型、运算符、字符串、类型转换 |
| `02_control_flow.py` | 控制流 | `if/elif/else`、`for`、`while`、`break/continue`、`match/case` |
| `03_functions.py` | 函数 | 定义、默认参数、`*args/**kwargs`、lambda、递归、高阶函数 |
| `04_data_structures.py` | 数据结构 | 列表、元组、字典、集合及推导式 |
| `05_oop.py` | 面向对象 | 类、继承、封装、多态、`@property`、类方法、静态方法 |
| `06_error_handling.py` | 异常处理 | `try/except/else/finally`、自定义异常、`assert` |
| `07_file_io.py` | 文件读写 | 文本文件、JSON、CSV、`os.path` 路径操作 |

## PyTorch 学习示例

本仓库还包含 PyTorch 深度学习入门示例，需要先安装依赖：

```bash
pip install torch numpy
```

| 文件 | 主题 | 核心内容 |
|------|------|----------|
| `torch_01_tensors.py` | 张量基础 | 创建、索引、切片、形状变换、数学运算、NumPy 互转 |
| `torch_02_autograd.py` | 自动微分 | `requires_grad`、`backward()`、梯度累积、`no_grad`、手动梯度下降 |
| `torch_03_nn_basics.py` | 神经网络基础 | `nn.Sequential`、自定义 `nn.Module`、激活函数、损失函数、优化器 |
| `torch_04_training_loop.py` | 完整训练流程 | 训练/验证循环、`train()`/`eval()`、学习率调度、最佳模型保存 |
| `torch_05_dataset_dataloader.py` | 数据集与加载 | 自定义 `Dataset`、`DataLoader`、`random_split`、数据变换 |
| `torch_06_cnn.py` | 卷积神经网络 | `Conv2d`、`MaxPool2d`、`BatchNorm2d`、`Dropout`、特征图追踪 |
| `torch_07_save_load.py` | 模型保存加载 | `state_dict`、整个模型、训练 Checkpoint、推理一致性验证 |

## 运行方式

```bash
# Python 基础示例
python 01_basics.py
python 02_control_flow.py
# ... 以此类推

# PyTorch 示例
python torch_01_tensors.py
python torch_02_autograd.py
# ... 以此类推
```

> 建议按文件编号顺序学习，每个文件都可以独立运行。
