# Python 面向对象编程（OOP）
# Python Object-Oriented Programming

# ── 1. 类的基础定义 ──────────────────────────────────────────────
print("=== 基础类 ===")

class Animal:
    """动物基类"""

    # 类变量（所有实例共享）
    kingdom = "动物界"

    def __init__(self, name, age):
        # 实例变量
        self.name = name
        self.age = age

    def speak(self):
        return f"{self.name} 发出了声音"

    def info(self):
        return f"{self.name}（{self.age}岁）属于{self.kingdom}"

    def __str__(self):
        return f"Animal({self.name})"

    def __repr__(self):
        return f"Animal(name={self.name!r}, age={self.age!r})"


dog = Animal("小黑", 3)
cat = Animal("咪咪", 5)

print(dog.info())
print(cat.speak())
print(str(dog))
print(repr(cat))
print(f"类变量: Animal.kingdom = {Animal.kingdom}")

# ── 2. 继承 ──────────────────────────────────────────────────────
print("\n=== 继承 ===")

class Dog(Animal):
    """狗：继承自 Animal"""

    def __init__(self, name, age, breed):
        super().__init__(name, age)  # 调用父类 __init__
        self.breed = breed

    def speak(self):                 # 重写（覆盖）父类方法
        return f"{self.name} 说：汪汪！"

    def fetch(self, item):
        return f"{self.name} 叼回了 {item}"

    def info(self):
        base = super().info()        # 复用父类方法
        return f"{base}，品种：{self.breed}"


class Cat(Animal):
    """猫：继承自 Animal"""

    def __init__(self, name, age, indoor=True):
        super().__init__(name, age)
        self.indoor = indoor

    def speak(self):
        return f"{self.name} 说：喵～"

    def info(self):
        location = "室内" if self.indoor else "室外"
        return f"{super().info()}，{location}猫"


rex = Dog("Rex", 2, "德国牧羊犬")
whiskers = Cat("Whiskers", 4)

print(rex.info())
print(rex.speak())
print(rex.fetch("球"))
print(whiskers.info())
print(whiskers.speak())

# isinstance / issubclass
print(f"\nisinstance(rex, Dog):    {isinstance(rex, Dog)}")
print(f"isinstance(rex, Animal): {isinstance(rex, Animal)}")
print(f"issubclass(Dog, Animal): {issubclass(Dog, Animal)}")

# ── 3. 封装：属性与私有变量 ──────────────────────────────────────
print("\n=== 封装 ===")

class BankAccount:
    """银行账户，演示封装"""

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance     # 双下划线 = 私有属性

    @property
    def balance(self):               # getter
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return f"存入 ¥{amount}，余额: ¥{self.__balance}"
        return "存款金额必须大于0"

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"取出 ¥{amount}，余额: ¥{self.__balance}"
        return "余额不足或金额无效"

    def __str__(self):
        return f"账户[{self.owner}] 余额: ¥{self.__balance}"


acc = BankAccount("Alice", 1000)
print(acc)
print(acc.deposit(500))
print(acc.withdraw(200))
print(f"余额（通过property）: ¥{acc.balance}")

# ── 4. 类方法与静态方法 ──────────────────────────────────────────
print("\n=== 类方法 & 静态方法 ===")

class Circle:
    pi = 3.14159265358979

    def __init__(self, radius):
        self.radius = radius

    def area(self):                          # 实例方法
        return self.pi * self.radius ** 2

    def perimeter(self):
        return 2 * self.pi * self.radius

    @classmethod
    def from_diameter(cls, diameter):        # 类方法：替代构造器
        return cls(diameter / 2)

    @staticmethod
    def is_valid_radius(r):                  # 静态方法：与类相关的工具函数
        return r > 0

    def __str__(self):
        return f"Circle(r={self.radius})"


c1 = Circle(5)
c2 = Circle.from_diameter(10)
print(f"{c1}: 面积={c1.area():.2f}, 周长={c1.perimeter():.2f}")
print(f"{c2}: 面积={c2.area():.2f}")
print(f"半径 -1 合法? {Circle.is_valid_radius(-1)}")
print(f"半径  5 合法? {Circle.is_valid_radius(5)}")

# ── 5. 多态 ──────────────────────────────────────────────────────
print("\n=== 多态 ===")

animals = [Dog("Buddy", 1, "金毛"), Cat("Luna", 3, indoor=False), Animal("小鸟", 1)]

for animal in animals:
    print(f"  {animal.speak()}")   # 相同接口，不同行为
