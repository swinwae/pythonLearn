# PyTorch 基础：张量（Tensor）
# PyTorch Basics: Tensors

import torch
import numpy as np

print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}\n")

# ── 1. 创建张量 ──────────────────────────────────────────────────
print("=== 创建张量 ===")

# 从 Python 列表创建
t1 = torch.tensor([1, 2, 3, 4, 5])
t2 = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print(f"1D 张量: {t1}")
print(f"2D 张量:\n{t2}")
print(f"t1 dtype: {t1.dtype}, t2 dtype: {t2.dtype}")

# 特殊张量
zeros  = torch.zeros(3, 4)
ones   = torch.ones(2, 3)
eye    = torch.eye(3)             # 单位矩阵
rand   = torch.rand(2, 3)        # 均匀分布 [0,1)
randn  = torch.randn(2, 3)       # 标准正态分布
arange = torch.arange(0, 10, 2)  # 类似 range
linsp  = torch.linspace(0, 1, 5) # 等间距

print(f"\nzeros(3,4):\n{zeros}")
print(f"ones(2,3):\n{ones}")
print(f"eye(3):\n{eye}")
print(f"rand(2,3):\n{rand}")
print(f"arange(0,10,2): {arange}")
print(f"linspace(0,1,5): {linsp}")

# ── 2. 张量属性 ──────────────────────────────────────────────────
print("\n=== 张量属性 ===")
t = torch.randn(3, 4)
print(f"张量:\n{t}")
print(f"shape:  {t.shape}")
print(f"size(): {t.size()}")
print(f"ndim:   {t.ndim}")
print(f"dtype:  {t.dtype}")
print(f"device: {t.device}")
print(f"numel:  {t.numel()}")   # 元素总数

# ── 3. 索引与切片 ────────────────────────────────────────────────
print("\n=== 索引与切片 ===")
m = torch.tensor([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
print(f"矩阵:\n{m}")
print(f"m[0]:       {m[0]}")        # 第0行
print(f"m[1, 2]:    {m[1, 2]}")     # 第1行第2列
print(f"m[:, 1]:    {m[:, 1]}")     # 第1列
print(f"m[0:2, 1:]: \n{m[0:2, 1:]}")  # 子矩阵
print(f"bool mask:  {m[m > 5]}")    # 布尔索引

# ── 4. 形状变换 ──────────────────────────────────────────────────
print("\n=== 形状变换 ===")
x = torch.arange(12)
print(f"原始: {x}")
print(f"reshape(3,4):\n{x.reshape(3, 4)}")
print(f"reshape(2,6):\n{x.reshape(2, 6)}")
print(f"reshape(2,2,3):\n{x.reshape(2, 2, 3)}")

# squeeze / unsqueeze
t = torch.randn(3, 4)
print(f"\n原始 shape: {t.shape}")
t_unsq = t.unsqueeze(0)   # 在第0维增加维度
print(f"unsqueeze(0): {t_unsq.shape}")
t_sq = t_unsq.squeeze(0)  # 去掉大小为1的维度
print(f"squeeze(0):   {t_sq.shape}")

# permute / transpose
t3d = torch.randn(2, 3, 4)
print(f"\n3D shape: {t3d.shape}")
print(f"permute(2,0,1): {t3d.permute(2, 0, 1).shape}")
print(f"transpose(0,1): {t3d.transpose(0, 1).shape}")

# ── 5. 数学运算 ──────────────────────────────────────────────────
print("\n=== 数学运算 ===")
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])

print(f"a + b = {a + b}")
print(f"a * b = {a * b}")       # 逐元素乘
print(f"a @ b = {a @ b}")       # 点积（内积）
print(f"a.dot(b) = {a.dot(b)}")

# 矩阵乘法
A = torch.randn(2, 3)
B = torch.randn(3, 4)
C = A @ B                       # 矩阵乘法
print(f"\nA{list(A.shape)} @ B{list(B.shape)} = C{list(C.shape)}")

# 聚合运算
t = torch.tensor([[1.0, 2.0, 3.0],
                   [4.0, 5.0, 6.0]])
print(f"\n张量:\n{t}")
print(f"sum():       {t.sum()}")
print(f"sum(dim=0):  {t.sum(dim=0)}")   # 按列求和
print(f"sum(dim=1):  {t.sum(dim=1)}")   # 按行求和
print(f"mean():      {t.mean():.4f}")
print(f"max():       {t.max()}")
print(f"min():       {t.min()}")
print(f"std():       {t.std():.4f}")
print(f"argmax():    {t.argmax()}")

# ── 6. 与 NumPy 互转 ─────────────────────────────────────────────
print("\n=== 与 NumPy 互转 ===")
np_arr = np.array([1.0, 2.0, 3.0])
t_from_np = torch.from_numpy(np_arr)   # 共享内存
t_clone   = torch.tensor(np_arr)       # 拷贝

print(f"NumPy -> Tensor: {t_from_np}")
back_to_np = t_from_np.numpy()
print(f"Tensor -> NumPy: {back_to_np}")

# 共享内存验证
np_arr[0] = 99
print(f"修改 numpy 后 tensor: {t_from_np}")   # 同步变化
print(f"clone 不受影响:       {t_clone}")

# ── 7. 原地操作（in-place）────────────────────────────────────────
print("\n=== 原地操作 ===")
t = torch.tensor([1.0, 2.0, 3.0])
print(f"原始: {t}")
t.add_(10)      # 带下划线的方法是原地操作
print(f"add_(10): {t}")
t.mul_(2)
print(f"mul_(2):  {t}")
