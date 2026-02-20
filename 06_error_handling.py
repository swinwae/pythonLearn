# Python 异常处理
# Python Error Handling

# ── 1. 基础 try / except ─────────────────────────────────────────
print("=== 基础 try/except ===")

def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "错误：除数不能为零"
    else:
        return f"{a} / {b} = {result}"   # 无异常时执行
    finally:
        pass                              # 无论如何都执行

print(safe_divide(10, 2))
print(safe_divide(10, 0))

# ── 2. 捕获多种异常 ──────────────────────────────────────────────
print("\n=== 捕获多种异常 ===")

def parse_integer(s):
    try:
        return int(s)
    except ValueError:
        return f"'{s}' 不是有效的整数"
    except TypeError:
        return f"类型错误：不能将 {type(s).__name__} 转换为整数"

print(parse_integer("42"))
print(parse_integer("abc"))
print(parse_integer(None))

# 用元组同时捕获多个异常
def safe_index(lst, idx):
    try:
        return lst[idx]
    except (IndexError, TypeError) as e:
        return f"访问错误: {e}"

data = [10, 20, 30]
print(safe_index(data, 1))
print(safe_index(data, 10))
print(safe_index(data, "a"))

# ── 3. 捕获所有异常并打印信息 ────────────────────────────────────
print("\n=== 捕获异常信息 ===")

def risky_operation(x):
    try:
        result = 100 / x + int("bad")
    except Exception as e:
        print(f"异常类型: {type(e).__name__}")
        print(f"异常信息: {e}")

risky_operation(0)

# ── 4. 自定义异常 ────────────────────────────────────────────────
print("\n=== 自定义异常 ===")

class AgeError(ValueError):
    """年龄无效时抛出"""
    def __init__(self, age, message=None):
        self.age = age
        self.message = message or f"年龄 {age} 不合法（必须在 0~150 之间）"
        super().__init__(self.message)


class InsufficientFundsError(Exception):
    """余额不足时抛出"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"余额不足：当前 ¥{balance}，需要 ¥{amount}")


def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"年龄必须是整数，收到 {type(age).__name__}")
    if not 0 <= age <= 150:
        raise AgeError(age)
    return f"年龄设置为 {age}"


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


for test_age in [25, -5, 200, "old"]:
    try:
        print(set_age(test_age))
    except AgeError as e:
        print(f"AgeError: {e}")
    except TypeError as e:
        print(f"TypeError: {e}")

try:
    remaining = withdraw(500, 800)
except InsufficientFundsError as e:
    print(f"InsufficientFundsError: {e}")

# ── 5. finally 与上下文管理器 ─────────────────────────────────────
print("\n=== finally 的使用 ===")

def open_resource():
    resource = "数据库连接"
    try:
        print(f"  打开 {resource}")
        # 模拟错误
        raise RuntimeError("操作失败")
    except RuntimeError as e:
        print(f"  捕获错误: {e}")
    finally:
        print(f"  关闭 {resource}（finally 保证执行）")

open_resource()

# ── 6. 使用 assert 进行断言 ──────────────────────────────────────
print("\n=== assert 断言 ===")

def calculate_bmi(weight_kg, height_m):
    assert weight_kg > 0, "体重必须为正数"
    assert height_m > 0, "身高必须为正数"
    bmi = weight_kg / height_m ** 2
    return round(bmi, 1)

try:
    print(f"BMI: {calculate_bmi(70, 1.75)}")
    print(f"BMI: {calculate_bmi(-10, 1.75)}")
except AssertionError as e:
    print(f"断言错误: {e}")
