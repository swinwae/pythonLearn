# PyTorch 数据集与数据加载器
# PyTorch Dataset and DataLoader

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np

torch.manual_seed(0)

# ── 1. 自定义 Dataset ────────────────────────────────────────────
print("=== 自定义 Dataset ===")

class SineWaveDataset(Dataset):
    """正弦波回归数据集：输入 x，预测 sin(x) + 噪声"""

    def __init__(self, n_samples=500, noise=0.1):
        self.x = torch.linspace(-2 * np.pi, 2 * np.pi, n_samples).unsqueeze(1)
        self.y = torch.sin(self.x) + noise * torch.randn_like(self.x)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


dataset = SineWaveDataset(n_samples=500, noise=0.1)
print(f"数据集大小: {len(dataset)}")
x0, y0 = dataset[0]
print(f"第0条样本: x={x0.item():.4f}, y={y0.item():.4f}")

# ── 2. 划分数据集 ────────────────────────────────────────────────
print("\n=== 划分数据集 ===")

train_size = int(0.7 * len(dataset))
val_size   = int(0.15 * len(dataset))
test_size  = len(dataset) - train_size - val_size

train_ds, val_ds, test_ds = random_split(dataset, [train_size, val_size, test_size])
print(f"训练集: {len(train_ds)}, 验证集: {len(val_ds)}, 测试集: {len(test_ds)}")

# ── 3. DataLoader ────────────────────────────────────────────────
print("\n=== DataLoader ===")

train_loader = DataLoader(train_ds, batch_size=32, shuffle=True,  num_workers=0)
val_loader   = DataLoader(val_ds,   batch_size=32, shuffle=False, num_workers=0)
test_loader  = DataLoader(test_ds,  batch_size=32, shuffle=False, num_workers=0)

print(f"训练批次数: {len(train_loader)}")
print(f"验证批次数: {len(val_loader)}")

x_batch, y_batch = next(iter(train_loader))
print(f"一批数据: x.shape={x_batch.shape}, y.shape={y_batch.shape}")

# ── 4. 带数据变换的 Dataset（transforms）────────────────────────
print("\n=== 带变换的 Dataset ===")

class NormalizingDataset(Dataset):
    """带归一化的数据集包装器"""

    def __init__(self, base_dataset):
        # 计算均值和标准差（用于归一化）
        all_x = torch.stack([base_dataset[i][0] for i in range(len(base_dataset))])
        self.mean = all_x.mean()
        self.std  = all_x.std()
        self.base = base_dataset

    def __len__(self):
        return len(self.base)

    def __getitem__(self, idx):
        x, y = self.base[idx]
        x_norm = (x - self.mean) / self.std   # Z-score 归一化
        return x_norm, y


norm_dataset = NormalizingDataset(dataset)
x_raw, _  = dataset[100]
x_norm, _ = norm_dataset[100]
print(f"原始 x[100]: {x_raw.item():.4f}")
print(f"归一化后:    {x_norm.item():.4f}")
print(f"mean={norm_dataset.mean:.4f}, std={norm_dataset.std:.4f}")

# ── 5. 端到端：在正弦数据上训练回归模型 ──────────────────────────
print("\n=== 端到端训练：拟合 sin(x) ===")

class SineNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, 64), nn.Tanh(),
            nn.Linear(64, 64), nn.Tanh(),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        return self.net(x)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SineNet().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

norm_train_ds = NormalizingDataset(train_ds.dataset)

# 重新创建归一化 DataLoader
def make_loader(indices, dataset, **kwargs):
    subset = torch.utils.data.Subset(dataset, indices)
    return DataLoader(subset, **kwargs)

norm_dl = DataLoader(
    torch.utils.data.Subset(norm_dataset, train_ds.indices),
    batch_size=32, shuffle=True
)
norm_val_dl = DataLoader(
    torch.utils.data.Subset(norm_dataset, val_ds.indices),
    batch_size=32
)

print(f"{'Epoch':>5} {'Train MSE':>10} {'Val MSE':>10}")
print("-" * 30)

for epoch in range(1, 31):
    model.train()
    train_loss = 0.0
    for xb, yb in norm_dl:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * len(xb)
    train_loss /= len(norm_dl.dataset)

    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for xb, yb in norm_val_dl:
            xb, yb = xb.to(device), yb.to(device)
            val_loss += criterion(model(xb), yb).item() * len(xb)
    val_loss /= len(norm_val_dl.dataset)

    if epoch % 10 == 0 or epoch == 1:
        print(f"{epoch:5d} {train_loss:10.6f} {val_loss:10.6f}")

print("\n训练完成！模型已学会拟合正弦波。")
