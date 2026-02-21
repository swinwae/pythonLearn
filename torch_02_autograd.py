# PyTorch 自动微分（Autograd）
# PyTorch Autograd: Automatic Differentiation

import torch

# ── 1. requires_grad 与梯度计算 ──────────────────────────────────
print("=== requires_grad 基础 ===")

x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x + 1   # y = x² + 2x + 1

print(f"x = {x}")
print(f"y = x² + 2x + 1 = {y}")

y.backward()   # 反向传播，计算 dy/dx

# dy/dx = 2x + 2，x=3 时 = 8
print(f"dy/dx at x=3: {x.grad}")   # 应为 8.0

# ── 2. 多变量梯度 ────────────────────────────────────────────────
print("\n=== 多变量梯度 ===")

a = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(3.0, requires_grad=True)

# z = a³ + b²
z = a ** 3 + b ** 2
print(f"a={a.item()}, b={b.item()}")
print(f"z = a³ + b² = {z.item()}")

z.backward()

# dz/da = 3a² = 12, dz/db = 2b = 6
print(f"dz/da = 3a² = {a.grad.item()}")   # 12
print(f"dz/db = 2b  = {b.grad.item()}")   # 6

# ── 3. 向量的梯度（grad_outputs）────────────────────────────────
print("\n=== 向量梯度 ===")

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2 * 2   # y = [2, 8, 18]
print(f"x = {x.data}")
print(f"y = 2x² = {y.data}")

# 对向量求导需要传入 grad_tensors（权重向量）
y.backward(torch.ones_like(y))
# dy/dx = 4x，x=[1,2,3] → grad=[4,8,12]
print(f"dy/dx = 4x = {x.grad}")

# ── 4. 梯度累积与清零 ────────────────────────────────────────────
print("\n=== 梯度累积与清零 ===")

x = torch.tensor(2.0, requires_grad=True)

for i in range(3):
    y = x ** 2
    y.backward()
    print(f"第{i+1}次 backward 后 x.grad = {x.grad}")  # 梯度会累积！

# 清零梯度
x.grad.zero_()
print(f"zero_() 后 x.grad = {x.grad}")

# ── 5. 计算图与 no_grad ───────────────────────────────────────────
print("\n=== torch.no_grad() ===")

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

# 推理阶段不需要梯度，节省内存
with torch.no_grad():
    y = x * 2
    print(f"no_grad 内: y.requires_grad = {y.requires_grad}")

y2 = x * 2
print(f"no_grad 外: y2.requires_grad = {y2.requires_grad}")

# detach() 从计算图中分离
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
x_detach = x.detach()
print(f"\nx.requires_grad = {x.requires_grad}")
print(f"x.detach().requires_grad = {x_detach.requires_grad}")

# ── 6. 链式法则示例（手动验证）──────────────────────────────────
print("\n=== 链式法则验证 ===")

# 目标：f(x) = sin(x²)，df/dx = 2x·cos(x²)
import math

x = torch.tensor(math.pi / 4, requires_grad=True)
f = torch.sin(x ** 2)
f.backward()

auto_grad = x.grad.item()
manual_grad = 2 * x.item() * math.cos(x.item() ** 2)

print(f"x = π/4 ≈ {x.item():.4f}")
print(f"f(x) = sin(x²) = {f.item():.4f}")
print(f"自动微分 df/dx = {auto_grad:.6f}")
print(f"手动计算 2x·cos(x²) = {manual_grad:.6f}")
print(f"误差: {abs(auto_grad - manual_grad):.2e}")

# ── 7. 简单梯度下降（手动实现）──────────────────────────────────
print("\n=== 手动梯度下降：最小化 f(x) = (x-3)² ===")

x = torch.tensor(0.0, requires_grad=True)
lr = 0.1

for step in range(20):
    f = (x - 3) ** 2       # 最小值在 x=3
    f.backward()

    with torch.no_grad():
        x -= lr * x.grad   # 梯度更新
    x.grad.zero_()         # 清零梯度

    if step % 4 == 0:
        print(f"  step {step:2d}: x={x.item():.4f}, f(x)={f.item():.4f}")

print(f"最终 x = {x.item():.4f}（真实最优解: 3.0）")
