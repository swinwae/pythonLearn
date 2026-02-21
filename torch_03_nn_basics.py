# PyTorch 神经网络基础：nn.Module
# PyTorch Neural Network Basics: nn.Module

import torch
import torch.nn as nn
import torch.nn.functional as F

# ── 1. 内置层介绍 ────────────────────────────────────────────────
print("=== 常用内置层 ===")

# 线性层（全连接层）
linear = nn.Linear(in_features=4, out_features=2)
x = torch.randn(3, 4)   # batch_size=3, features=4
out = linear(x)
print(f"Linear(4→2): 输入{list(x.shape)} → 输出{list(out.shape)}")
print(f"  权重 shape: {linear.weight.shape}")
print(f"  偏置 shape: {linear.bias.shape}")

# 激活函数
x_act = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
print(f"\n输入:    {x_act.tolist()}")
print(f"ReLU:    {F.relu(x_act).tolist()}")
print(f"Sigmoid: {[round(v,3) for v in torch.sigmoid(x_act).tolist()]}")
print(f"Tanh:    {[round(v,3) for v in torch.tanh(x_act).tolist()]}")

# Softmax（用于多分类输出）
logits = torch.tensor([1.0, 2.0, 3.0])
probs = F.softmax(logits, dim=0)
print(f"\nlogits:  {logits.tolist()}")
print(f"softmax: {[round(v,3) for v in probs.tolist()]} (和={probs.sum():.1f})")

# ── 2. 用 nn.Sequential 快速搭建模型 ─────────────────────────────
print("\n=== nn.Sequential ===")

model = nn.Sequential(
    nn.Linear(8, 16),
    nn.ReLU(),
    nn.Linear(16, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
    nn.Sigmoid(),
)

print(model)
x = torch.randn(5, 8)
out = model(x)
print(f"\n输入 shape: {x.shape}")
print(f"输出 shape: {out.shape}")

# 参数统计
total = sum(p.numel() for p in model.parameters())
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"总参数量: {total}, 可训练: {trainable}")

# ── 3. 自定义 nn.Module ──────────────────────────────────────────
print("\n=== 自定义 nn.Module ===")

class MLP(nn.Module):
    """多层感知机（MLP）示例"""

    def __init__(self, input_dim, hidden_dim, output_dim, dropout=0.2):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout)
        self.bn = nn.BatchNorm1d(hidden_dim)   # 批归一化

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.bn(x)
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


mlp = MLP(input_dim=10, hidden_dim=32, output_dim=3)
print(mlp)

x = torch.randn(4, 10)   # batch=4, features=10
mlp.train()               # 训练模式（dropout 生效）
out_train = mlp(x)

mlp.eval()                # 评估模式（dropout 关闭）
with torch.no_grad():
    out_eval = mlp(x)

print(f"\n输入 shape:  {x.shape}")
print(f"输出 shape:  {out_train.shape}")

# ── 4. 损失函数 ──────────────────────────────────────────────────
print("\n=== 常用损失函数 ===")

# 二分类：BCELoss
pred_binary = torch.sigmoid(torch.randn(5, 1))
target_binary = torch.randint(0, 2, (5, 1)).float()
bce_loss = nn.BCELoss()(pred_binary, target_binary)
print(f"BCELoss:            {bce_loss.item():.4f}")

# 二分类（带 logits，更稳定）：BCEWithLogitsLoss
logits = torch.randn(5, 1)
bce_logits_loss = nn.BCEWithLogitsLoss()(logits, target_binary)
print(f"BCEWithLogitsLoss:  {bce_logits_loss.item():.4f}")

# 多分类：CrossEntropyLoss
pred_multi = torch.randn(5, 3)    # 5样本，3类
target_multi = torch.randint(0, 3, (5,))
ce_loss = nn.CrossEntropyLoss()(pred_multi, target_multi)
print(f"CrossEntropyLoss:   {ce_loss.item():.4f}")

# 回归：MSELoss / L1Loss / SmoothL1Loss
pred_reg = torch.randn(5)
target_reg = torch.randn(5)
mse  = nn.MSELoss()(pred_reg, target_reg)
l1   = nn.L1Loss()(pred_reg, target_reg)
huber = nn.SmoothL1Loss()(pred_reg, target_reg)
print(f"MSELoss:            {mse.item():.4f}")
print(f"L1Loss:             {l1.item():.4f}")
print(f"SmoothL1Loss:       {huber.item():.4f}")

# ── 5. 优化器 ────────────────────────────────────────────────────
print("\n=== 常用优化器 ===")

model = MLP(10, 32, 1)

# 常用优化器
sgd   = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
adam  = torch.optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.999))
adamw = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)

print("SGD:   ", sgd)
print("Adam:  ", adam)
print("AdamW: ", adamw)

# 学习率调度器
scheduler = torch.optim.lr_scheduler.StepLR(adam, step_size=5, gamma=0.5)
print("\n学习率调度（每5步减半）:")
for epoch in range(1, 16):
    # 模拟一次训练（先 optimizer.step，再 scheduler.step）
    optimizer.step()
    scheduler.step()
    if epoch % 5 == 0:
        lr = scheduler.get_last_lr()[0]
        print(f"  epoch {epoch:2d}: lr = {lr:.6f}")
