# Python 基础：变量、数据类型与运算符
# Python Basics: Variables, Data Types, and Operators

# ── 1. 变量与赋值 ───────────────────────────────────────────────
name = "Alice"          # 字符串 str
age = 25                # 整数 int
height = 1.68           # 浮点数 float
is_student = True       # 布尔 bool

print("=== 变量 ===")
print(f"姓名: {name}, 年龄: {age}, 身高: {height}, 是学生: {is_student}")
print(f"类型: {type(name)}, {type(age)}, {type(height)}, {type(is_student)}")

# ── 2. 数字运算 ──────────────────────────────────────────────────
print("\n=== 数字运算 ===")
a, b = 17, 5
print(f"加法: {a} + {b} = {a + b}")
print(f"减法: {a} - {b} = {a - b}")
print(f"乘法: {a} * {b} = {a * b}")
print(f"除法: {a} / {b} = {a / b}")        # 浮点除
print(f"整除: {a} // {b} = {a // b}")       # 整数除
print(f"取余: {a} % {b} = {a % b}")
print(f"幂运算: {a} ** {b} = {a ** b}")

# ── 3. 字符串操作 ────────────────────────────────────────────────
print("\n=== 字符串操作 ===")
s = "Hello, Python!"
print(f"原字符串: {s}")
print(f"长度: {len(s)}")
print(f"大写: {s.upper()}")
print(f"小写: {s.lower()}")
print(f"替换: {s.replace('Python', 'World')}")
print(f"分割: {s.split(', ')}")
print(f"切片 [0:5]: {s[0:5]}")
print(f"反转: {s[::-1]}")

# ── 4. 多重赋值与类型转换 ─────────────────────────────────────────
print("\n=== 类型转换 ===")
x, y, z = 1, 2, 3
print(f"多重赋值: x={x}, y={y}, z={z}")

num_str = "42"
num_int = int(num_str)      # str -> int
num_float = float(num_str)  # str -> float
back_to_str = str(num_int)  # int -> str
print(f"str -> int: {num_int}, 类型: {type(num_int)}")
print(f"str -> float: {num_float}, 类型: {type(num_float)}")

# ── 5. 比较与逻辑运算符 ──────────────────────────────────────────
print("\n=== 比较与逻辑 ===")
p, q = 10, 20
print(f"{p} > {q}: {p > q}")
print(f"{p} < {q}: {p < q}")
print(f"{p} == {q}: {p == q}")
print(f"{p} != {q}: {p != q}")
print(f"True and False: {True and False}")
print(f"True or False: {True or False}")
print(f"not True: {not True}")
