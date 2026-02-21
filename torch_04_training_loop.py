# PyTorch 完整训练流程
# PyTorch Complete Training Loop

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(42)

# ── 1. 生成合成数据集 ─────────────────────────────────────────────
print("=== 生成合成数据 ===")

# 二分类：y = 1 if x0 + x1 > 0 else 0（加噪声）
N = 1000
X = torch.randn(N, 2)
y = ((X[:, 0] + X[:, 1]) > 0).long()

# 划分训练/验证集（8:2）
split = int(0.8 * N)
X_train, X_val = X[:split], X[split:]
y_train, y_val = y[:split], y[split:]

train_ds = TensorDataset(X_train, y_train)
val_ds   = TensorDataset(X_val, y_val)

train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_ds,   batch_size=32, shuffle=False)

print(f"训练集: {len(train_ds)} 样本, {len(train_loader)} 批次")
print(f"验证集: {len(val_ds)} 样本, {len(val_loader)} 批次")

# ── 2. 定义模型 ──────────────────────────────────────────────────
print("\n=== 模型 ===")

class BinaryClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 2),
        )

    def forward(self, x):
        return self.net(x)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BinaryClassifier().to(device)
print(model)

# ── 3. 训练配置 ──────────────────────────────────────────────────
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)

# ── 4. 训练与验证函数 ─────────────────────────────────────────────

def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, total_correct, total = 0.0, 0, 0

    for X_batch, y_batch in loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)

        optimizer.zero_grad()        # 1. 清零梯度
        logits = model(X_batch)      # 2. 前向传播
        loss = criterion(logits, y_batch)  # 3. 计算损失
        loss.backward()              # 4. 反向传播
        optimizer.step()             # 5. 更新参数

        preds = logits.argmax(dim=1)
        total_loss    += loss.item() * len(y_batch)
        total_correct += (preds == y_batch).sum().item()
        total         += len(y_batch)

    return total_loss / total, total_correct / total


def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss, total_correct, total = 0.0, 0, 0

    with torch.no_grad():
        for X_batch, y_batch in loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            logits = model(X_batch)
            loss = criterion(logits, y_batch)

            preds = logits.argmax(dim=1)
            total_loss    += loss.item() * len(y_batch)
            total_correct += (preds == y_batch).sum().item()
            total         += len(y_batch)

    return total_loss / total, total_correct / total


# ── 5. 训练循环 ──────────────────────────────────────────────────
print("\n=== 训练开始 ===")
print(f"{'Epoch':>5} {'Train Loss':>11} {'Train Acc':>10} {'Val Loss':>9} {'Val Acc':>9} {'LR':>10}")
print("-" * 62)

EPOCHS = 20
history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
best_val_acc = 0.0
best_state = None

for epoch in range(1, EPOCHS + 1):
    tr_loss, tr_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
    va_loss, va_acc = evaluate(model, val_loader, criterion, device)
    scheduler.step()
    lr = scheduler.get_last_lr()[0]

    history["train_loss"].append(tr_loss)
    history["val_loss"].append(va_loss)
    history["train_acc"].append(tr_acc)
    history["val_acc"].append(va_acc)

    if va_acc > best_val_acc:
        best_val_acc = va_acc
        best_state = {k: v.clone() for k, v in model.state_dict().items()}

    if epoch % 5 == 0 or epoch == 1:
        print(f"{epoch:5d} {tr_loss:11.4f} {tr_acc:9.1%} {va_loss:9.4f} {va_acc:9.1%} {lr:10.6f}")

print("-" * 62)
print(f"最佳验证准确率: {best_val_acc:.1%}")

# ── 6. 恢复最佳模型并推理 ────────────────────────────────────────
print("\n=== 最佳模型推理 ===")
model.load_state_dict(best_state)
model.eval()

sample = torch.tensor([[1.5, 0.5], [-1.0, -1.5], [0.2, -0.3]]).to(device)
with torch.no_grad():
    logits = model(sample)
    probs  = F.softmax(logits, dim=1)
    preds  = logits.argmax(dim=1)

true_labels = [(x[0] + x[1] > 0).int().item() for x in sample]
print(f"{'输入':>20} {'预测':>4} {'真实':>4} {'P(1)':>8}")
for i in range(len(sample)):
    x = sample[i].tolist()
    print(f"[{x[0]:5.1f}, {x[1]:5.1f}] {preds[i].item():>4d} {true_labels[i]:>4d} {probs[i,1].item():>8.3f}")
