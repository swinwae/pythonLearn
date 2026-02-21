# PyTorch 模型保存与加载
# PyTorch Model Save and Load

import torch
import torch.nn as nn
import os

SAVE_DIR = "/tmp/torch_demo_models"
os.makedirs(SAVE_DIR, exist_ok=True)

# ── 辅助模型定义 ─────────────────────────────────────────────────
class SimpleNet(nn.Module):
    def __init__(self, input_dim=4, hidden=16, output_dim=2):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden)
        self.fc2 = nn.Linear(hidden, output_dim)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


# ── 1. 保存 / 加载 state_dict（推荐方式）────────────────────────
print("=== 方式1：state_dict（推荐）===")

model = SimpleNet()
print("原始权重 fc1.bias:", model.fc1.bias.data)

# 保存
path_sd = os.path.join(SAVE_DIR, "model_state.pth")
torch.save(model.state_dict(), path_sd)
print(f"state_dict 已保存: {path_sd}")
print(f"文件大小: {os.path.getsize(path_sd)} bytes")

# 加载：必须先实例化同结构模型
model2 = SimpleNet()
model2.load_state_dict(torch.load(path_sd, weights_only=True))
model2.eval()
print("加载后 fc1.bias:", model2.fc1.bias.data)
print("权重一致:", torch.equal(model.fc1.bias, model2.fc1.bias))

# ── 2. 保存 / 加载整个模型（含结构）────────────────────────────
print("\n=== 方式2：保存整个模型 ===")

path_full = os.path.join(SAVE_DIR, "model_full.pth")
torch.save(model, path_full)
print(f"整个模型已保存: {path_full}")

model3 = torch.load(path_full, weights_only=False)
model3.eval()
print(f"加载类型: {type(model3).__name__}")
print("权重一致:", torch.equal(model.fc1.weight, model3.fc1.weight))

# ── 3. 保存训练 Checkpoint（含优化器状态）────────────────────────
print("\n=== 方式3：训练 Checkpoint ===")

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)

# 模拟训练5轮
for _ in range(5):
    dummy_loss = torch.tensor(1.0, requires_grad=True)
    dummy_loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    scheduler.step()

checkpoint = {
    "epoch": 5,
    "model_state": model.state_dict(),
    "optimizer_state": optimizer.state_dict(),
    "scheduler_state": scheduler.state_dict(),
    "best_val_loss": 0.35,
    "config": {"input_dim": 4, "hidden": 16, "output_dim": 2},
}

path_ckpt = os.path.join(SAVE_DIR, "checkpoint_epoch5.pth")
torch.save(checkpoint, path_ckpt)
print(f"Checkpoint 已保存: {path_ckpt}")
print(f"文件大小: {os.path.getsize(path_ckpt)} bytes")

# 恢复 Checkpoint
ckpt = torch.load(path_ckpt, weights_only=False)
cfg = ckpt["config"]
resumed_model = SimpleNet(cfg["input_dim"], cfg["hidden"], cfg["output_dim"])
resumed_model.load_state_dict(ckpt["model_state"])

resumed_opt = torch.optim.Adam(resumed_model.parameters())
resumed_opt.load_state_dict(ckpt["optimizer_state"])

print(f"从 epoch {ckpt['epoch']} 恢复，best_val_loss={ckpt['best_val_loss']}")
print(f"当前 lr: {resumed_opt.param_groups[0]['lr']:.6f}")

# ── 4. 推理验证：保存前后输出一致 ────────────────────────────────
print("\n=== 验证保存前后推理一致 ===")

torch.manual_seed(0)
x_test = torch.randn(3, 4)

model.eval()
model2.eval()
model3.eval()
resumed_model.eval()

with torch.no_grad():
    out_orig    = model(x_test)
    out_sd      = model2(x_test)
    out_full    = model3(x_test)
    out_resumed = resumed_model(x_test)

print(f"原始输出:     {out_orig[0].tolist()}")
print(f"state_dict:   {out_sd[0].tolist()}")
print(f"整个模型:     {out_full[0].tolist()}")
print(f"checkpoint:   {out_resumed[0].tolist()}")

all_equal = (
    torch.allclose(out_orig, out_sd) and
    torch.allclose(out_orig, out_full) and
    torch.allclose(out_orig, out_resumed)
)
print(f"\n四种方式输出完全一致: {all_equal}")

# ── 5. 清理 ──────────────────────────────────────────────────────
import shutil
shutil.rmtree(SAVE_DIR)
print(f"\n临时文件已清理: {SAVE_DIR}")
