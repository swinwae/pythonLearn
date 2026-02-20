# Python 控制流：条件判断与循环
# Python Control Flow: Conditionals and Loops

# ── 1. if / elif / else ──────────────────────────────────────────
print("=== if / elif / else ===")
score = 82

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"分数 {score} 对应等级: {grade}")

# 三元表达式（条件表达式）
age = 20
status = "成年" if age >= 18 else "未成年"
print(f"年龄 {age}: {status}")

# ── 2. for 循环 ──────────────────────────────────────────────────
print("\n=== for 循环 ===")

# 遍历 range
print("range(5):", end=" ")
for i in range(5):
    print(i, end=" ")
print()

# 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"  水果: {fruit}")

# enumerate 同时获取索引和值
print("enumerate 示例:")
for idx, fruit in enumerate(fruits, start=1):
    print(f"  {idx}. {fruit}")

# ── 3. while 循环 ────────────────────────────────────────────────
print("\n=== while 循环 ===")
count = 0
while count < 5:
    print(f"  count = {count}")
    count += 1

# ── 4. break / continue / else ──────────────────────────────────
print("\n=== break & continue ===")
print("遇到 3 就停止:")
for n in range(10):
    if n == 3:
        break
    print(f"  {n}", end=" ")
print()

print("跳过偶数:")
for n in range(10):
    if n % 2 == 0:
        continue
    print(f"  {n}", end=" ")
print()

# for...else：循环正常结束（未被 break）时执行 else
print("\nfor...else 示例:")
for n in range(5):
    if n == 10:   # 不会触发
        break
else:
    print("  循环正常结束，没有 break")

# ── 5. 嵌套循环：九九乘法表 ─────────────────────────────────────
print("\n=== 九九乘法表 ===")
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end="\t")
    print()

# ── 6. match/case（Python 3.10+）───────────────────────────────
print("\n=== match / case (Python 3.10+) ===")
def describe_type(value):
    match value:
        case int():
            return f"{value} 是整数"
        case str():
            return f"'{value}' 是字符串"
        case list():
            return f"{value} 是列表，长度 {len(value)}"
        case _:
            return f"{value} 是其他类型"

for v in [42, "hello", [1, 2, 3], 3.14]:
    print(f"  {describe_type(v)}")
