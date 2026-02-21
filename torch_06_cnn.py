# PyTorch 卷积神经网络（CNN）
# PyTorch Convolutional Neural Network

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(42)

# ── 1. 卷积层基础 ─────────────────────────────────────────────────
print("=== 卷积层基础 ===")

# Conv2d(in_channels, out_channels, kernel_size)
conv = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, padding=1)

# 模拟一批灰度图 batch=2, C=1, H=8, W=8
img = torch.randn(2, 1, 8, 8)
out = conv(img)
print(f"输入:  {img.shape}  (batch, C_in, H, W)")
print(f"输出:  {out.shape}  (batch, C_out, H', W')")
print(f"权重:  {conv.weight.shape}  (C_out, C_in, kH, kW)")

# 池化层
pool = nn.MaxPool2d(kernel_size=2, stride=2)
pooled = pool(out)
print(f"\nMaxPool2d(2): {out.shape} → {pooled.shape}")

avg_pool = nn.AvgPool2d(2, 2)
print(f"AvgPool2d(2): {out.shape} → {avg_pool(out).shape}")

# 不同 padding / stride
print("\n不同参数的 Conv2d 输出尺寸（输入 32×32）:")
for k, p, s in [(3, 0, 1), (3, 1, 1), (3, 1, 2), (5, 2, 1)]:
    c = nn.Conv2d(1, 1, kernel_size=k, padding=p, stride=s)
    x = torch.randn(1, 1, 32, 32)
    o = c(x)
    print(f"  k={k}, pad={p}, stride={s} → {o.shape[-2]}×{o.shape[-1]}")

# ── 2. 定义 CNN 模型（模拟 MNIST 结构）───────────────────────────
print("\n=== CNN 模型（类 LeNet）===")

class SimpleCNN(nn.Module):
    """
    类 LeNet 结构，处理 1×28×28 的灰度图像（10分类）
    输入: (N, 1, 28, 28)
    输出: (N, 10)
    """
    def __init__(self, num_classes=10):
        super().__init__()
        # 卷积块 1
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),  # 28×28
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),                              # 14×14
        )
        # 卷积块 2
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1), # 14×14
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),                              # 7×7
        )
        # 全局平均池化（代替 Flatten+全连接）
        self.gap = nn.AdaptiveAvgPool2d(1)               # 1×1
        # 分类器
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.gap(x)
        x = self.classifier(x)
        return x


model = SimpleCNN(num_classes=10)
print(model)

x = torch.randn(4, 1, 28, 28)
out = model(x)
print(f"\n输入 shape:  {x.shape}")
print(f"输出 shape:  {out.shape}")

total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"可训练参数:  {total_params:,}")

# ── 3. 特征图可视化（形状追踪）──────────────────────────────────
print("\n=== 特征图形状追踪 ===")

class DebugCNN(nn.Module):
    def forward(self, x):
        print(f"  输入:      {tuple(x.shape)}")
        x = nn.Conv2d(1, 32, 3, padding=1)(x);  print(f"  conv1:     {tuple(x.shape)}")
        x = F.relu(x)
        x = F.max_pool2d(x, 2);                  print(f"  pool1:     {tuple(x.shape)}")
        x = nn.Conv2d(32, 64, 3, padding=1)(x);  print(f"  conv2:     {tuple(x.shape)}")
        x = F.relu(x)
        x = F.max_pool2d(x, 2);                  print(f"  pool2:     {tuple(x.shape)}")
        x = F.adaptive_avg_pool2d(x, 1);         print(f"  gap:       {tuple(x.shape)}")
        x = x.flatten(1);                         print(f"  flatten:   {tuple(x.shape)}")
        return x

debug = DebugCNN()
_ = debug(torch.randn(1, 1, 28, 28))

# ── 4. 在合成数据上训练 CNN ───────────────────────────────────────
print("\n=== 合成数据训练 CNN ===")

# 生成随机 "图像" 数据（模拟 MNIST 结构）
N, C, H, W, CLASSES = 400, 1, 28, 28, 10
X_data = torch.randn(N, C, H, W)
y_data = torch.randint(0, CLASSES, (N,))

split = int(0.8 * N)
train_ds = TensorDataset(X_data[:split], y_data[:split])
val_ds   = TensorDataset(X_data[split:], y_data[split:])

train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_ds,   batch_size=32)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

print(f"{'Epoch':>5} {'Train Loss':>11} {'Train Acc':>10} {'Val Acc':>9}")
print("-" * 42)

for epoch in range(1, 11):
    model.train()
    tr_loss, tr_correct, tr_total = 0.0, 0, 0
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        logits = model(xb)
        loss = criterion(logits, yb)
        loss.backward()
        optimizer.step()
        tr_loss    += loss.item() * len(yb)
        tr_correct += (logits.argmax(1) == yb).sum().item()
        tr_total   += len(yb)

    model.eval()
    va_correct, va_total = 0, 0
    with torch.no_grad():
        for xb, yb in val_loader:
            xb, yb = xb.to(device), yb.to(device)
            va_correct += (model(xb).argmax(1) == yb).sum().item()
            va_total   += len(yb)

    if epoch % 2 == 0 or epoch == 1:
        print(f"{epoch:5d} {tr_loss/tr_total:11.4f} {tr_correct/tr_total:9.1%} {va_correct/va_total:9.1%}")
