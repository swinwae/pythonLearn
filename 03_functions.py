# Python 函数
# Python Functions

# ── 1. 基础函数定义与调用 ─────────────────────────────────────────
print("=== 基础函数 ===")

def greet(name):
    """向指定姓名的人打招呼"""
    return f"你好，{name}！"

print(greet("Alice"))
print(greet("Bob"))

# ── 2. 默认参数 ──────────────────────────────────────────────────
print("\n=== 默认参数 ===")

def power(base, exponent=2):
    """计算 base 的 exponent 次方，默认平方"""
    return base ** exponent

print(f"power(3)   = {power(3)}")       # 使用默认值 exponent=2
print(f"power(3,3) = {power(3, 3)}")

# ── 3. 关键字参数 ────────────────────────────────────────────────
print("\n=== 关键字参数 ===")

def describe_person(name, age, city="未知"):
    return f"{name}，{age}岁，来自{city}"

print(describe_person("Alice", 25, city="北京"))
print(describe_person(age=30, name="Bob"))   # 顺序无关

# ── 4. 可变参数 *args 与 **kwargs ────────────────────────────────
print("\n=== *args 与 **kwargs ===")

def sum_all(*args):
    """接受任意数量的数字并求和"""
    return sum(args)

print(f"sum_all(1,2,3)     = {sum_all(1, 2, 3)}")
print(f"sum_all(1,2,3,4,5) = {sum_all(1, 2, 3, 4, 5)}")

def print_info(**kwargs):
    """打印任意键值对信息"""
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="Alice", age=25, hobby="编程")

# ── 5. 返回多个值 ────────────────────────────────────────────────
print("\n=== 返回多个值 ===")

def min_max(numbers):
    """返回列表的最小值和最大值"""
    return min(numbers), max(numbers)

data = [3, 1, 4, 1, 5, 9, 2, 6]
lo, hi = min_max(data)
print(f"数据: {data}")
print(f"最小值: {lo}, 最大值: {hi}")

# ── 6. Lambda 函数（匿名函数）────────────────────────────────────
print("\n=== Lambda 函数 ===")

square = lambda x: x ** 2
add = lambda x, y: x + y

print(f"square(7) = {square(7)}")
print(f"add(3, 4) = {add(3, 4)}")

# 配合 sorted/map/filter 使用
numbers = [5, 2, 8, 1, 9, 3]
print(f"原始: {numbers}")
print(f"排序: {sorted(numbers)}")
print(f"按平方排序: {sorted(numbers, key=lambda x: x**2)}")
print(f"偶数: {list(filter(lambda x: x % 2 == 0, numbers))}")
print(f"各元素×2: {list(map(lambda x: x * 2, numbers))}")

# ── 7. 递归 ──────────────────────────────────────────────────────
print("\n=== 递归 ===")

def factorial(n):
    """计算 n 的阶乘"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    """返回斐波那契数列第 n 项"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(1, 8):
    print(f"  {i}! = {factorial(i)}")

fib_seq = [fibonacci(i) for i in range(10)]
print(f"斐波那契(0~9): {fib_seq}")

# ── 8. 内置高阶函数 ──────────────────────────────────────────────
print("\n=== 内置高阶函数 ===")
from functools import reduce

nums = [1, 2, 3, 4, 5]
print(f"map(×2):    {list(map(lambda x: x*2, nums))}")
print(f"filter(偶): {list(filter(lambda x: x%2==0, nums))}")
print(f"reduce(+):  {reduce(lambda a, b: a+b, nums)}")
