# ==================== product.py ====================
# 商品类
class Product:
    total_count = 0  # 商品总数，用来统计一共创建了多少个商品

    def __init__(self, pid, name, price):
        self.pid = pid  # 商品ID，每个商品唯一
        self.name = name  # 商品名称
        self.price = price  # 商品价格
        self.stock = 0  # 库存，一开始都是0，后面再加
        Product.total_count += 1  # 每创建一个商品就加1

    # 改价格，之前忘记加判断了
    def change_price(self, new_price):
        if new_price <= 0:
            print("价格不能是负数啊")
            return False
        self.price = new_price
        return True

    # 加库存，进货的时候用
    def add_stock(self, num):
        if num > 0:
            self.stock += num
            return True
        return False

    # 卖出商品，要检查库存够不够
    def sell(self, num):
        if num > 0 and num <= self.stock:
            self.stock -= num
            return True
        return False

    @classmethod
    def get_total(cls):
        return cls.total_count

    @staticmethod
    def to_money(amount):
        # 把数字转成金额格式，比如 5.5 变成 $5.50
        return f"${amount:.2f}"

    def __str__(self):
        # 打印商品信息的时候用
        return f"{self.pid}\t{self.name}\t{self.to_money(self.price)}\t库存:{self.stock}"


# ==================== people.py ====================
# Person是基类，User和Staff都继承它
class Person:
    def __init__(self, name, pwd):
        self.name = name  # 用户名
        self.pwd = pwd  # 密码，以后要考虑加密

    # 检查密码对不对
    def check_pwd(self, pwd):
        return self.pwd == pwd

    def __str__(self):
        return self.name


# 用户类 - 改了无数次了
class User(Person):
    user_count = 0  # 统计有多少用户

    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.cart = []  # 购物车，里面放的是(商品, 数量)的元组
        User.user_count += 1

    # 加入购物车，搞了好久才写对
    def add_to_cart(self, product, num=1):
        # 先看看购物车里有没有这个商品，有的话就增加数量
        for i, (p, qty) in enumerate(self.cart):
            if p.pid == product.pid:
                self.cart[i] = (p, qty + num)
                return
        # 没有的话就加新的
        self.cart.append((product, num))

    # 从购物车删除商品
    def remove_from_cart(self, pid):
        # 这里用列表推导式也可以，但怕写错，就用循环了
        new_cart = []
        for p, qty in self.cart:
            if p.pid != pid:
                new_cart.append((p, qty))
        self.cart = new_cart

    # 清空购物车，结账后调用
    def clear_cart(self):
        self.cart = []

    # 计算购物车总价
    def cart_total(self):
        total = 0
        for p, qty in self.cart:
            total += p.price * qty
        return total

    # 显示购物车内容
    def show_cart(self):
        if not self.cart:
            return "购物车空的"

        s = "购物车内容:\n"
        for p, qty in self.cart:
            s += f"  {p.name} x{qty} = {Product.to_money(p.price * qty)}\n"
        s += f"总计: {Product.to_money(self.cart_total())}"
        return s

    @classmethod
    def get_count(cls):
        return cls.user_count


# 员工类
class Staff(Person):
    staff_count = 0  # 统计有多少员工

    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        Staff.staff_count += 1
        self.staff_id = Staff.staff_count  # 工号按注册顺序生成

    @classmethod
    def get_count(cls):
        return cls.staff_count

    def __str__(self):
        return f"{self.name} (工号:{self.staff_id})"


# ==================== history.py ====================
# 购买记录 - 本来想用字典的，还是写个类吧
class History:
    def __init__(self, pid, name, price, num):
        self.pid = pid  # 商品ID
        self.name = name  # 商品名称
        self.price = price  # 当时购买的价格
        self.num = num  # 购买数量
        self.buy_time = self.get_time()  # 购买时间

    @staticmethod
    def get_time():
        # 获取当前时间，精确到秒
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 计算这笔交易的总价
    def total(self):
        return self.price * self.num

    def __str__(self):
        return f"{self.buy_time} - {self.name} x{self.num} = {Product.to_money(self.total())}"


# ==================== file_helper.py ====================
# 文件操作，抄来抄去搞了好久
class FileHelper:
    # 文件路径，放在这里方便改
    PRODUCT_FILE = "products.txt"
    USER_FILE = "users.txt"
    STAFF_FILE = "staff.txt"
    SALES_FILE = "sales.txt"

    @staticmethod
    def read_lines(path):
        # 读取文件，返回每一行的列表
        try:
            f = open(path, 'r', encoding='UTF-8')
            lines = f.readlines()
            f.close()
            return lines
        except FileNotFoundError:
            # 文件不存在就创建空的
            f = open(path, 'w', encoding='UTF-8')
            f.close()
            return []
        except:
            # 其他错误就打印一下
            print(f"读取{path}出错")
            return []

    @staticmethod
    def write_lines(path, lines):
        # 写入文件，会覆盖原有内容
        try:
            f = open(path, 'w', encoding='UTF-8')
            f.writelines(lines)
            f.close()
        except:
            print(f"写入{path}出错")

    @staticmethod
    def append_line(path, line):
        # 在文件末尾追加一行
        try:
            f = open(path, 'a', encoding='UTF-8')
            f.write(line)
            f.close()
        except:
            print(f"追加{path}出错")

    # 加载商品 - 这里改了好几次
    @classmethod
    def load_products(cls):
        lines = cls.read_lines(cls.PRODUCT_FILE)
        prods = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split('|')
            if len(parts) >= 3:
                try:
                    pid = int(parts[0])
                    name = parts[1]
                    price = float(parts[2])
                    p = Product(pid, name, price)

                    if len(parts) >= 4:
                        p.stock = int(parts[3])

                    prods.append(p)
                    # 更新总数，这样新商品ID不会重复
                    if p.pid > Product.total_count:
                        Product.total_count = p.pid
                except:
                    # 跳过格式不对的行
                    continue

        return prods

    @classmethod
    def save_products(cls, prods):
        # 保存所有商品到文件
        lines = []
        for p in prods:
            lines.append(f"{p.pid}|{p.name}|{p.price}|{p.stock}\n")
        cls.write_lines(cls.PRODUCT_FILE, lines)

    @classmethod
    def load_users(cls):
        # 加载用户列表
        lines = cls.read_lines(cls.USER_FILE)
        users = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split('|')
            if len(parts) >= 2:
                users.append(User(parts[0], parts[1]))

        return users

    @classmethod
    def save_users(cls, users):
        # 保存用户列表
        lines = []
        for u in users:
            lines.append(f"{u.name}|{u.pwd}\n")
        cls.write_lines(cls.USER_FILE, lines)

    @classmethod
    def load_staff(cls):
        # 加载员工列表
        lines = cls.read_lines(cls.STAFF_FILE)
        staff = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split('|')
            if len(parts) >= 2:
                s = Staff(parts[0], parts[1])
                staff.append(s)
                # 更新工号计数
                if s.staff_id > Staff.staff_count:
                    Staff.staff_count = s.staff_id

        return staff

    @classmethod
    def save_staff(cls, staff):
        # 保存员工列表
        lines = []
        for s in staff:
            lines.append(f"{s.name}|{s.pwd}\n")
        cls.write_lines(cls.STAFF_FILE, lines)

    @classmethod
    def add_sale(cls, pid, name, price, num):
        # 添加一条销售记录
        line = f"{pid}\t{name}\t{price}\t{num}\n"
        cls.append_line(cls.SALES_FILE, line)

    @classmethod
    def get_sales(cls):
        # 获取所有销售记录
        lines = cls.read_lines(cls.SALES_FILE)
        sales = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            if len(parts) >= 4:
                try:
                    sales.append({
                        'pid': parts[0],
                        'name': parts[1],
                        'price': float(parts[2]),
                        'num': int(parts[3])
                    })
                except:
                    continue

        return sales


# ==================== staff_side.py ====================
# 员工端功能 - 这里代码有点乱，但能用
class StaffManager:
    def __init__(self, prods, staff):
        self.prods = prods  # 商品列表
        self.staff = staff  # 员工列表
        self.me = None  # 当前登录的员工

    def login(self):
        # 员工登录，有三次机会
        print("\n======= 员工登录 =======")

        for i in range(3):
            name = input("用户名：")
            pwd = input("密码：")

            for s in self.staff:
                if s.name == name and s.check_pwd(pwd):
                    self.me = s
                    print("登录成功！")
                    return True

            if i < 2:
                print(f"还剩{2 - i}次机会")

        print("登录失败")
        return False

    def register(self):
        # 注册新员工
        print("\n======= 员工注册 =======")

        while True:
            name = input("新用户名：")
            exist = False
            for s in self.staff:
                if s.name == name:
                    exist = True
                    break
            if not exist:
                break
            print("用户名已经被用了")

        pwd = input("密码：")
        pwd2 = input("确认密码：")

        if pwd != pwd2:
            print("两次密码不一样")
            return False

        new_staff = Staff(name, pwd)
        self.staff.append(new_staff)
        FileHelper.save_staff(self.staff)
        print(f"注册成功！工号{new_staff.staff_id}")
        return True

    def menu(self):
        # 员工主菜单
        while True:
            print("\n" + "=" * 40)
            print(f"员工：{self.me.name} 工号：{self.me.staff_id}")
            print("=" * 40)
            print("1. 添加商品")
            print("2. 删除商品")
            print("3. 修改商品")
            print("4. 查看所有商品")
            print("5. 查看销售记录")
            print("6. 生成销售报告")
            print("0. 退出登录")
            print("-" * 40)

            c = input("请选择：")

            if c == '1':
                self.add_prod()
            elif c == '2':
                self.del_prod()
            elif c == '3':
                self.edit_prod()
            elif c == '4':
                self.show_prods()
            elif c == '5':
                self.show_sales()
            elif c == '6':
                self.sales_rpt()
            elif c == '0':
                # 退出前保存数据
                FileHelper.save_products(self.prods)
                print("已退出")
                break
            else:
                print("没这个选项")

    def show_prods(self):
        # 显示所有商品
        if not self.prods:
            print("还没有商品")
            return

        print("\n" + "=" * 40)
        print("商品列表")
        print("=" * 40)
        print("编号\t名称\t价格\t库存")
        print("-" * 40)

        for p in self.prods:
            print(p)

        print("=" * 40)
        print(f"共{len(self.prods)}种商品")

    def find_prod(self, pid):
        # 根据ID查找商品
        for p in self.prods:
            if p.pid == pid:
                return p
        return None

    def add_prod(self):
        # 添加新商品
        print("\n--- 添加商品 ---")

        name = input("商品名称：")
        if not name:
            print("名称不能空")
            return

        try:
            price = float(input("价格："))
            if price <= 0:
                print("价格要大于0")
                return
        except:
            print("请输入数字")
            return

        try:
            stock = int(input("库存："))
            if stock < 0:
                print("库存不能是负数")
                return
        except:
            print("库存输入不对")
            return

        # 生成新ID，取最大ID+1
        if self.prods:
            new_id = max([p.pid for p in self.prods]) + 1
        else:
            new_id = 1

        p = Product(new_id, name, price)
        p.stock = stock
        self.prods.append(p)
        print(f"商品'{name}'添加成功，ID{new_id}")

    def del_prod(self):
        # 删除商品
        print("\n--- 删除商品 ---")

        try:
            pid = int(input("商品编号："))
        except:
            print("编号不对")
            return

        p = self.find_prod(pid)
        if not p:
            print("没这个商品")
            return

        print(f"找到：{p}")
        sure = input("确定删除？(y/n)：")
        if sure.lower() == 'y':
            self.prods.remove(p)
            print("已删除")

    def edit_prod(self):
        # 修改商品信息
        print("\n--- 修改商品 ---")

        try:
            pid = int(input("商品编号："))
        except:
            print("编号不对")
            return

        p = self.find_prod(pid)
        if not p:
            print("没这个商品")
            return

        print(f"当前信息：{p}")
        print("-" * 20)

        # 修改价格
        new_price = input("新价格(回车不改)：")
        if new_price:
            try:
                if p.change_price(float(new_price)):
                    print("价格已改")
                else:
                    print("价格不对")
            except:
                print("价格格式错误")

        # 修改库存
        new_stock = input("新库存(回车不改)：")
        if new_stock:
            try:
                p.stock = int(new_stock)
                print("库存已改")
            except:
                print("库存格式错误")

        print("修改完成")

    def show_sales(self):
        # 显示销售记录
        print("\n--- 销售记录 ---")

        sales = FileHelper.get_sales()
        if not sales:
            print("还没有销售记录")
            return

        print("编号\t名称\t单价\t数量\t总价")
        print("-" * 50)

        total = 0
        for s in sales:
            t = s['price'] * s['num']
            total += t
            print(f"{s['pid']}\t{s['name']}\t{s['price']}\t{s['num']}\t{Product.to_money(t)}")

        print("-" * 50)
        print(f"总收入：{Product.to_money(total)}")

    def sales_rpt(self):
        # 生成销售报告
        print("\n" + "=" * 50)
        print("销售报告")
        print("=" * 50)

        print(f"商品总数：{Product.get_total()}")
        print(f"现有商品：{len(self.prods)}种")

        # 计算库存总价值
        if self.prods:
            total_val = 0
            for p in self.prods:
                total_val += p.price * p.stock
            print(f"库存总值：{Product.to_money(total_val)}")

        # 销售统计
        sales = FileHelper.get_sales()
        if sales:
            total_num = len(sales)
            total_money = 0
            for s in sales:
                total_money += s['price'] * s['num']

            print(f"\n销售单数：{total_num}")
            print(f"销售总额：{Product.to_money(total_money)}")

        print("=" * 50)


# ==================== user_side.py ====================
# 用户端功能 - 这部分写得比较急
class UserManager:
    def __init__(self, prods, users, his):
        self.prods = prods  # 商品列表
        self.users = users  # 用户列表
        self.his = his  # 购买历史
        self.me = None  # 当前登录的用户

    def login(self):
        # 用户登录
        print("\n======= 用户登录 =======")

        for i in range(3):
            name = input("用户名：")
            pwd = input("密码：")

            for u in self.users:
                if u.name == name and u.check_pwd(pwd):
                    self.me = u
                    print("登录成功！")
                    return True

            if i < 2:
                print(f"还剩{2 - i}次机会")

        print("登录失败")
        return False

    def register(self):
        # 注册新用户
        print("\n======= 用户注册 =======")

        while True:
            name = input("新用户名：")
            exist = False
            for u in self.users:
                if u.name == name:
                    exist = True
                    break
            if not exist:
                break
            print("用户名已存在")

        pwd = input("密码：")
        pwd2 = input("确认密码：")

        if pwd != pwd2:
            print("两次密码不一样")
            return False

        self.users.append(User(name, pwd))
        FileHelper.save_users(self.users)
        print("注册成功！")
        return True

    def menu(self):
        # 用户主菜单
        while True:
            print("\n" + "=" * 40)
            print(f"欢迎 {self.me.name}")
            print("=" * 40)
            print("1. 浏览商品")
            print("2. 搜索商品")
            print("3. 查看购物车")
            print("4. 加入购物车")
            print("5. 结账")
            print("6. 购买历史")
            print("0. 退出")
            print("-" * 40)

            c = input("请选择：")

            if c == '1':
                self.show_prods()
            elif c == '2':
                self.search_prods()
            elif c == '3':
                self.show_cart()
            elif c == '4':
                self.add_cart()
            elif c == '5':
                self.checkout()
            elif c == '6':
                self.show_his()
            elif c == '0':
                break
            else:
                print("没这个选项")

    def show_prods(self):
        # 显示所有商品
        if not self.prods:
            print("暂无商品")
            return

        print("\n" + "=" * 40)
        print("商品列表")
        print("=" * 40)
        print("编号\t名称\t价格\t库存")
        print("-" * 40)

        for p in self.prods:
            print(p)

        print("=" * 40)

    def search_prods(self):
        # 根据关键字搜索商品
        kw = input("输入关键字：").lower()

        res = []
        for p in self.prods:
            if kw in p.name.lower():
                res.append(p)

        if res:
            print(f"\n找到{len(res)}个：")
            for p in res:
                print(p)
        else:
            print("没找到")

    def find_prod(self, pid):
        # 根据ID查找商品
        for p in self.prods:
            if p.pid == pid:
                return p
        return None

    def show_cart(self):
        # 显示购物车
        print("\n" + "=" * 40)
        print(self.me.show_cart())
        print("=" * 40)

    def add_cart(self):
        # 添加商品到购物车
        try:
            pid = int(input("商品编号："))
        except:
            print("编号不对")
            return

        p = self.find_prod(pid)
        if not p:
            print("没这个商品")
            return

        print(f"商品：{p}")

        try:
            num = int(input("数量："))
            if num <= 0:
                print("数量要大于0")
                return
        except:
            print("数量不对")
            return

        if num > p.stock:
            print(f"库存不够，只剩{p.stock}")
            return

        self.me.add_to_cart(p, num)
        print("已加入购物车")

    def checkout(self):
        # 结账
        if not self.me.cart:
            print("购物车空的")
            return

        print("\n" + "=" * 40)
        print("结账")
        print("=" * 40)
        print(self.me.show_cart())

        total = self.me.cart_total()
        sure = input(f"总计{Product.to_money(total)}，确认？(y/n)：")

        if sure.lower() == 'y':
            # 更新库存并记录历史
            for p, num in self.me.cart:
                p.sell(num)
                self.his.append(History(p.pid, p.name, p.price, num))
                FileHelper.add_sale(p.pid, p.name, p.price, num)

            print("购买成功！")
            self.me.clear_cart()

    def show_his(self):
        # 显示购买历史，只显示最近10条
        if not self.his:
            print("暂无购买历史")
            return

        print("\n" + "=" * 40)
        print("购买历史")
        print("=" * 40)

        start = max(0, len(self.his) - 10)
        for i in range(start, len(self.his)):
            print(self.his[i])

        print("=" * 40)


# ==================== main.py ====================
def main():
    print("=" * 50)
    print("HKMU SUPERMARKET v1.0")
    print("=" * 50)

    # 加载数据
    products = FileHelper.load_products()
    staff = FileHelper.load_staff()
    users = FileHelper.load_users()
    history = []  # 历史记录存在内存里，不存文件

    # 如果没有员工，加一个默认的
    if not staff:
        print("首次运行，创建默认员工账号")
        staff.append(Staff("admin", "123456"))
        FileHelper.save_staff(staff)

    # 如果没有商品，给点示例数据
    if not products:
        print("添加一些示例商品")
        products.append(Product(1, "苹果", 5.5))
        products.append(Product(2, "香蕉", 3.0))
        products.append(Product(3, "可乐", 4.5))
        products[0].stock = 50
        products[1].stock = 30
        products[2].stock = 20
        FileHelper.save_products(products)

    # 如果没有用户，给个示例
    if not users:
        users.append(User("test", "123"))
        FileHelper.save_users(users)

    # 主循环
    while True:
        print("\n" + "=" * 40)
        print("请选择：")
        print("1. 员工登录")
        print("2. 用户登录")
        print("3. 注册用户")
        print("4. 注册员工")
        print("0. 退出")
        print("-" * 40)

        c = input("请选择：")

        if c == '1':
            sm = StaffManager(products, staff)
            if sm.login():
                sm.menu()

        elif c == '2':
            um = UserManager(products, users, history)
            if um.login():
                um.menu()

        elif c == '3':
            um = UserManager(products, users, history)
            if um.register():
                print("注册成功，请登录")

        elif c == '4':
            sm = StaffManager(products, staff)
            if sm.register():
                print("注册成功，请登录")

        elif c == '0':
            # 退出前保存所有数据
            FileHelper.save_products(products)
            FileHelper.save_users(users)
            FileHelper.save_staff(staff)
            print("欢迎再次光临！")
            break

        else:
            print("输入错误")


if __name__ == '__main__':
    main()