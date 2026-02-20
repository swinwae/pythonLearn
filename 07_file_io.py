# Python 文件读写
# Python File I/O

import os
import json
import csv

TEMP_DIR = "/tmp/python_learn_demo"
os.makedirs(TEMP_DIR, exist_ok=True)

# ── 1. 写入文本文件 ──────────────────────────────────────────────
print("=== 写入文本文件 ===")

txt_path = os.path.join(TEMP_DIR, "sample.txt")

lines = [
    "第一行：Python 文件读写示例\n",
    "第二行：使用 with 语句自动关闭文件\n",
    "第三行：open() 的 mode 参数控制读写模式\n",
]

with open(txt_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"已写入: {txt_path}")

# 追加写入
with open(txt_path, "a", encoding="utf-8") as f:
    f.write("第四行：追加写入（mode='a'）\n")

print("已追加一行")

# ── 2. 读取文本文件 ──────────────────────────────────────────────
print("\n=== 读取文本文件 ===")

# 一次性读取全部
with open(txt_path, "r", encoding="utf-8") as f:
    content = f.read()
print("全部内容:")
print(content)

# 逐行读取
with open(txt_path, "r", encoding="utf-8") as f:
    print("逐行读取:")
    for i, line in enumerate(f, start=1):
        print(f"  [{i}] {line}", end="")
print()

# 读取为列表
with open(txt_path, "r", encoding="utf-8") as f:
    all_lines = f.readlines()
print(f"共 {len(all_lines)} 行")

# ── 3. JSON 文件读写 ─────────────────────────────────────────────
print("\n=== JSON 文件读写 ===")

json_path = os.path.join(TEMP_DIR, "data.json")

students = [
    {"name": "Alice", "age": 20, "scores": [88, 92, 95]},
    {"name": "Bob",   "age": 22, "scores": [75, 80, 78]},
    {"name": "Carol", "age": 21, "scores": [95, 98, 100]},
]

# 写入 JSON
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(students, f, ensure_ascii=False, indent=2)
print(f"已写入 JSON: {json_path}")

# 读取 JSON
with open(json_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)

print("读取 JSON 数据:")
for s in loaded:
    avg = sum(s["scores"]) / len(s["scores"])
    print(f"  {s['name']}（{s['age']}岁）平均分: {avg:.1f}")

# ── 4. CSV 文件读写 ──────────────────────────────────────────────
print("\n=== CSV 文件读写 ===")

csv_path = os.path.join(TEMP_DIR, "products.csv")

products = [
    {"name": "苹果",   "price": 5.0,  "stock": 100},
    {"name": "香蕉",   "price": 3.5,  "stock": 200},
    {"name": "橙子",   "price": 4.0,  "stock": 150},
]

# 写入 CSV
fieldnames = ["name", "price", "stock"]
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)
print(f"已写入 CSV: {csv_path}")

# 读取 CSV
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("读取 CSV 数据:")
    for row in reader:
        print(f"  {row['name']}: ¥{row['price']}，库存 {row['stock']}")

# ── 5. 文件与路径操作 ────────────────────────────────────────────
print("\n=== os / os.path 操作 ===")

print(f"目录存在: {os.path.exists(TEMP_DIR)}")
print(f"是文件: {os.path.isfile(txt_path)}")
print(f"文件大小: {os.path.getsize(txt_path)} 字节")
print(f"文件名: {os.path.basename(txt_path)}")
print(f"目录名: {os.path.dirname(txt_path)}")
print(f"扩展名: {os.path.splitext(txt_path)[1]}")

print(f"\n{TEMP_DIR} 中的文件:")
for fname in os.listdir(TEMP_DIR):
    fpath = os.path.join(TEMP_DIR, fname)
    size = os.path.getsize(fpath)
    print(f"  {fname} ({size} B)")

# ── 6. 清理临时文件 ──────────────────────────────────────────────
print("\n=== 清理临时文件 ===")
import shutil
shutil.rmtree(TEMP_DIR)
print(f"已删除临时目录: {TEMP_DIR}")
