# Python 数据结构：列表、元组、字典、集合
# Python Data Structures: List, Tuple, Dict, Set

# ── 1. 列表 List ─────────────────────────────────────────────────
print("=== 列表 List ===")
nums = [3, 1, 4, 1, 5, 9, 2, 6]
fruits = ["苹果", "香蕉", "橙子"]

print(f"列表: {nums}")
print(f"索引[0]: {nums[0]}, 索引[-1]: {nums[-1]}")
print(f"切片[2:5]: {nums[2:5]}")
print(f"长度: {len(nums)}")
print(f"排序: {sorted(nums)}")
print(f"最大/最小: {max(nums)}/{min(nums)}")
print(f"求和: {sum(nums)}")
print(f"是否包含 5: {5 in nums}")

# 常用方法
fruits.append("葡萄")          # 末尾添加
fruits.insert(1, "草莓")       # 指定位置插入
fruits.remove("香蕉")          # 删除首个匹配
popped = fruits.pop()          # 弹出末尾
print(f"操作后: {fruits}, 弹出: {popped}")

# 列表推导式
squares = [x**2 for x in range(1, 6)]
evens = [x for x in range(20) if x % 2 == 0]
print(f"平方列表: {squares}")
print(f"偶数列表: {evens}")

# ── 2. 元组 Tuple ────────────────────────────────────────────────
print("\n=== 元组 Tuple ===")
point = (3, 4)
rgb = (255, 128, 0)
single = (42,)   # 单元素元组需要逗号

print(f"坐标: {point}, x={point[0]}, y={point[1]}")
print(f"RGB: {rgb}")
print(f"单元素元组: {single}, 类型: {type(single)}")

# 元组解包
x, y = point
print(f"解包: x={x}, y={y}")

a, *rest = (1, 2, 3, 4, 5)
print(f"解包带*: a={a}, rest={rest}")

# ── 3. 字典 Dict ─────────────────────────────────────────────────
print("\n=== 字典 Dict ===")
person = {
    "name": "Alice",
    "age": 25,
    "city": "北京",
    "hobbies": ["读书", "编程"]
}

print(f"姓名: {person['name']}")
print(f"年龄: {person.get('age')}")
print(f"职业(不存在): {person.get('job', '未知')}")

# 遍历字典
print("所有信息:")
for key, value in person.items():
    print(f"  {key}: {value}")

print(f"所有键: {list(person.keys())}")
print(f"所有值: {list(person.values())}")

# 添加 / 更新 / 删除
person["email"] = "alice@example.com"
person["age"] = 26
del person["city"]
print(f"更新后: {person}")

# 字典推导式
word_lengths = {w: len(w) for w in ["Python", "is", "awesome"]}
print(f"单词长度: {word_lengths}")

# ── 4. 集合 Set ──────────────────────────────────────────────────
print("\n=== 集合 Set ===")
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}

print(f"集合 a: {a}")
print(f"集合 b: {b}")
print(f"并集 a|b: {a | b}")
print(f"交集 a&b: {a & b}")
print(f"差集 a-b: {a - b}")
print(f"对称差 a^b: {a ^ b}")
print(f"a 是否为 b 的子集: {a.issubset(b)}")

# 去重
duplicates = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(duplicates))
print(f"去重前: {duplicates}")
print(f"去重后: {sorted(unique)}")

# ── 5. 综合示例：词频统计 ─────────────────────────────────────────
print("\n=== 综合示例：词频统计 ===")
text = "apple banana apple orange banana apple grape orange"
words = text.split()
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1

# 按频率排序
sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
print("词频统计（降序）:")
for word, count in sorted_freq:
    print(f"  {word}: {'█' * count} ({count})")
