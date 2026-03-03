# ==================== models/goods.py ====================
class Goods:
    """商品类"""
    # 类属性
    total_goods = 0
    category_list = ["食品", "饮料", "日用品", "电子产品"]

    def __init__(self, id, productName, productPrice, category="食品"):
        self.id = id  # 公开属性，方便使用
        self.productName = productName
        self.productPrice = productPrice
        self.category = category
        self.discount = 1.0
        self.stock = 0
        Goods.total_goods += 1

    # 实例方法
    def get_price(self):
        """获取实际价格（考虑折扣）"""
        return self.productPrice * self.discount

    def set_price(self, new_price):
        """设置价格"""
        if new_price > 0:
            self.productPrice = new_price
            return True
        return False

    def set_discount(self, discount):
        """设置折扣"""
        if 0 < discount <= 1:
            self.discount = discount
            return True
        return False

    def add_stock(self, quantity):
        """增加库存"""
        if quantity > 0:
            self.stock += quantity
            return True
        return False

    def reduce_stock(self, quantity):
        """减少库存"""
        if 0 < quantity <= self.stock:
            self.stock -= quantity
            return True
        return False

    # 类方法
    @classmethod
    def get_total_goods(cls):
        """获取商品总数"""
        return cls.total_goods

    @classmethod
    def get_categories(cls):
        """获取所有商品类别"""
        return cls.category_list.copy()

    @classmethod
    def add_category(cls, new_category):
        """添加新类别"""
        if new_category not in cls.category_list:
            cls.category_list.append(new_category)
            return True
        return False

    # 静态方法
    @staticmethod
    def format_currency(amount):
        """格式化货币"""
        return f"${amount:.2f}"

    @staticmethod
    def validate_price(price):
        """验证价格"""
        return price > 0

    # 保留基本的魔术方法，方便打印
    def __str__(self):
        discount_info = f" (折扣: {int((1 - self.discount) * 100)}% off)" if self.discount < 1 else ""
        return f"{self.id}\t{self.productName}\t{self.format_currency(self.get_price())}{discount_info}\t库存:{self.stock}"


# ==================== models/person.py ====================
class Person:
    """人员基类"""

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.login_attempts = 0
        self.is_active = True

    def verify_login(self, password):
        """验证登录"""
        if not self.is_active:
            print("账户已被禁用！")
            return False

        if self.password == password:
            self.login_attempts = 0
            return True
        else:
            self.login_attempts += 1
            if self.login_attempts >= 3:
                self.is_active = False
                print("登录失败次数过多，账户已被锁定！")
            return False

    def change_password(self, old_password, new_password):
        """修改密码"""
        if self.verify_login(old_password):
            self.password = new_password
            return True
        return False

    def __str__(self):
        return f"{self.name}"


# ==================== models/staff.py ====================
class Staff(Person):
    """员工类（继承自Person）"""
    staff_count = 0

    def __init__(self, staffname, staffpassword, position="员工"):
        super().__init__(staffname, staffpassword)
        self.position = position
        self.employee_id = self.generate_employee_id()
        self.salary = 0
        Staff.staff_count += 1

    @staticmethod
    def generate_employee_id():
        """生成员工ID"""
        import random
        return f"EMP{random.randint(1000, 9999)}"

    def get_role(self):
        """获取角色"""
        return f"员工-{self.position}"

    @classmethod
    def get_staff_count(cls):
        """获取员工总数"""
        return cls.staff_count

    def __str__(self):
        return f"{self.name} (工号:{self.employee_id}, 职位:{self.position})"


# ==================== models/user.py ====================
class User(Person):
    """用户类（继承自Person）"""
    user_count = 0

    def __init__(self, username, userpassword, vip_level=0):
        super().__init__(username, userpassword)
        self.vip_level = vip_level
        self.points = 0
        self.cart = []  # 购物车，存储(商品, 数量)
        User.user_count += 1

    def get_role(self):
        """获取角色"""
        return "VIP用户" if self.vip_level > 0 else "普通用户"

    def add_points(self, amount):
        """增加积分"""
        self.points += amount
        # 检查是否升级VIP
        if self.points >= 1000 and self.vip_level < 1:
            self.vip_level = 1
            print(f"恭喜！{self.name}升级为VIP用户！")

    def use_points(self, points):
        """使用积分"""
        if points <= self.points:
            self.points -= points
            return True
        return False

    # 购物车方法
    def add_to_cart(self, goods, quantity=1):
        """添加商品到购物车"""
        for i, (item, qty) in enumerate(self.cart):
            if item.id == goods.id:
                self.cart[i] = (item, qty + quantity)
                return
        self.cart.append((goods, quantity))

    def remove_from_cart(self, goods_id):
        """从购物车移除商品"""
        self.cart = [(item, qty) for item, qty in self.cart if item.id != goods_id]

    def clear_cart(self):
        """清空购物车"""
        self.cart.clear()

    def get_cart_total(self):
        """计算购物车总价"""
        total = 0
        for goods, qty in self.cart:
            total += goods.get_price() * qty
        return total

    def view_cart(self):
        """查看购物车"""
        if not self.cart:
            return "购物车是空的"

        result = "购物车内容:\n"
        for goods, qty in self.cart:
            result += f"  {goods.productName} x{qty} = {Goods.format_currency(goods.get_price() * qty)}\n"
        result += f"总计: {Goods.format_currency(self.get_cart_total())}"
        return result

    @classmethod
    def get_user_count(cls):
        """获取用户总数"""
        return cls.user_count


# ==================== models/history.py ====================
class History:
    """购买历史记录类"""

    def __init__(self, id, productName, productPrice, productNumber):
        self.id = id
        self.productName = productName
        self.productPrice = productPrice
        self.productNumber = productNumber
        self.purchase_time = self.get_current_time()

    @staticmethod
    def get_current_time():
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_total_price(self):
        """获取总价"""
        return self.productPrice * self.productNumber

    def __str__(self):
        return f"{self.purchase_time} - {self.productName} x{self.productNumber} = {Goods.format_currency(self.get_total_price())}"


# ==================== utils/file_handler.py ====================
class FileHandler:
    """文件处理类"""

    # 文件路径
    GOODS_PATH = "goods.txt"
    USER_PATH = "users.txt"
    STAFF_PATH = "staff.txt"
    HISTORY_PATH = "history.txt"
    SALES_PATH = "sales_history.txt"

    @staticmethod
    def read_file(filepath):
        """读取文件"""
        try:
            with open(filepath, 'r', encoding='UTF-8') as f:
                return f.readlines()
        except FileNotFoundError:
            # 文件不存在，创建空文件
            with open(filepath, 'w', encoding='UTF-8') as f:
                pass
            return []

    @staticmethod
    def write_file(filepath, lines):
        """写入文件"""
        with open(filepath, 'w', encoding='UTF-8') as f:
            f.writelines(lines)

    @staticmethod
    def append_file(filepath, line):
        """追加到文件"""
        with open(filepath, 'a', encoding='UTF-8') as f:
            f.write(line)

    # 商品文件操作
    @classmethod
    def read_goods(cls):
        """读取商品"""
        lines = cls.read_file(cls.GOODS_PATH)
        goods_list = []

        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 4:
                    try:
                        id = int(parts[0])
                        name = parts[1]
                        price = float(parts[2])
                        category = parts[3]
                        goods = Goods(id, name, price, category)

                        # 读取库存（如果有）
                        if len(parts) >= 5:
                            goods.stock = int(parts[4])

                        goods_list.append(goods)
                    except:
                        pass

        return goods_list

    @classmethod
    def write_goods(cls, goods_list):
        """写入商品"""
        lines = []
        for goods in goods_list:
            line = f"{goods.id}|{goods.productName}|{goods.productPrice}|{goods.category}|{goods.stock}\n"
            lines.append(line)
        cls.write_file(cls.GOODS_PATH, lines)

    # 用户文件操作
    @classmethod
    def read_users(cls):
        """读取用户"""
        lines = cls.read_file(cls.USER_PATH)
        user_list = []

        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 2:
                    user = User(parts[0], parts[1])
                    if len(parts) > 2:
                        try:
                            user.vip_level = int(parts[2])
                        except:
                            pass
                    if len(parts) > 3:
                        try:
                            user.points = int(parts[3])
                        except:
                            pass
                    user_list.append(user)

        return user_list

    @classmethod
    def write_users(cls, user_list):
        """写入用户"""
        lines = []
        for user in user_list:
            line = f"{user.name}|{user.password}|{user.vip_level}|{user.points}\n"
            lines.append(line)
        cls.write_file(cls.USER_PATH, lines)

    # 员工文件操作
    @classmethod
    def read_staff(cls):
        """读取员工"""
        lines = cls.read_file(cls.STAFF_PATH)
        staff_list = []

        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 2:
                    staff = Staff(parts[0], parts[1])
                    if len(parts) > 2:
                        staff.position = parts[2]
                    staff_list.append(staff)

        return staff_list

    @classmethod
    def write_staff(cls, staff_list):
        """写入员工"""
        lines = []
        for staff in staff_list:
            line = f"{staff.name}|{staff.password}|{staff.position}\n"
            lines.append(line)
        cls.write_file(cls.STAFF_PATH, lines)

    # 销售记录
    @classmethod
    def record_sale(cls, goods_id, goods_name, price, quantity):
        """记录销售"""
        line = f"{goods_id}\t{goods_name}\t{price}\t{quantity}\n"
        cls.append_file(cls.SALES_PATH, line)

    @classmethod
    def read_sales(cls):
        """读取销售记录"""
        lines = cls.read_file(cls.SALES_PATH)
        sales = []

        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('\t')
                if len(parts) >= 4:
                    sales.append({
                        'id': parts[0],
                        'name': parts[1],
                        'price': float(parts[2]),
                        'quantity': int(parts[3])
                    })

        return sales


# ==================== controllers/manager.py ====================
class Manager:
    """管理员类"""

    def __init__(self, goods_list, staff_list):
        self.goods_list = goods_list
        self.staff_list = staff_list
        self.current_staff = None

    def login(self):
        """登录"""
        print("\n======= 员工登录 =======")

        for attempt in range(3):
            name = input("请输入账户名称：")
            password = input("请输入账户密码：")

            for staff in self.staff_list:
                if staff.name == name and staff.verify_login(password):
                    self.current_staff = staff
                    print("========= 登录成功 =========")
                    return True

            if attempt < 2:
                print(f"账户名称或密码错误，您还有 {2 - attempt} 次机会")

        print("========= 登录失败 =========")
        return False

    def register(self):
        """注册新员工"""
        print("\n======= 员工注册 =======")

        # 输入用户名
        while True:
            name = input("请输入新员工名称：")
            # 检查是否已存在
            exists = False
            for staff in self.staff_list:
                if staff.name == name:
                    exists = True
                    break

            if not exists:
                break
            print("用户名已存在，请重新输入！")

        # 输入密码
        password = input("请输入密码：")
        repassword = input("请再次输入密码：")

        if password == repassword:
            new_staff = Staff(name, password)
            self.staff_list.append(new_staff)
            FileHandler.write_staff(self.staff_list)
            print("****** 员工注册成功 ******")
            return True
        else:
            print("两次密码不一致，注册失败！")
            return False

    def show_menu(self):
        """显示管理员菜单"""
        while True:
            print("\n" + "=" * 50)
            print("管理员菜单")
            print("=" * 50)
            print("1. 添加商品")
            print("2. 删除商品")
            print("3. 修改商品")
            print("4. 查看所有商品")
            print("5. 设置商品折扣")
            print("6. 查看销售记录")
            print("7. 生成销售报告")
            print("8. 管理员工")
            print("0. 退出")
            print("-" * 50)

            choice = input("请选择操作：")

            if choice == "1":
                self.add_goods()
            elif choice == "2":
                self.delete_goods()
            elif choice == "3":
                self.modify_goods()
            elif choice == "4":
                self.show_all_goods()
            elif choice == "5":
                self.set_discount()
            elif choice == "6":
                self.show_sales()
            elif choice == "7":
                self.generate_report()
            elif choice == "8":
                self.manage_staff()
            elif choice == "0":
                # 保存数据
                FileHandler.write_goods(self.goods_list)
                print("数据已保存，再见！")
                break
            else:
                print("无效选择，请重新输入！")

    def show_all_goods(self):
        """显示所有商品"""
        print("\n" + "=" * 50)
        print("商品列表")
        print("=" * 50)
        print("编号\t商品名称\t价格\t库存")
        print("-" * 50)

        for goods in self.goods_list:
            print(goods)

        print("=" * 50)
        print(f"总计: {len(self.goods_list)}种商品")

    def find_goods_by_id(self, goods_id):
        """通过ID查找商品"""
        for goods in self.goods_list:
            if goods.id == goods_id:
                return goods
        return None

    def add_goods(self):
        """添加商品"""
        print("\n--- 添加商品 ---")

        # 显示可用的类别
        print(f"可选类别: {Goods.get_categories()}")

        name = input("商品名称：")
        if not name:
            print("商品名称不能为空！")
            return

        try:
            price = float(input("商品价格："))
            if not Goods.validate_price(price):
                print("价格必须大于0！")
                return

            category = input("商品类别：")
            if category not in Goods.get_categories():
                print(f"类别'{category}'不存在，将使用默认类别'食品'")
                category = "食品"

            stock = int(input("初始库存："))
            if stock < 0:
                print("库存不能为负数！")
                return

            # 生成新ID
            if self.goods_list:
                new_id = max([g.id for g in self.goods_list]) + 1
            else:
                new_id = 1

            # 创建商品
            new_goods = Goods(new_id, name, price, category)
            new_goods.stock = stock

            self.goods_list.append(new_goods)
            print(f"✓ 商品 '{name}' 添加成功！")

        except ValueError:
            print("输入格式错误！")

    def delete_goods(self):
        """删除商品"""
        print("\n--- 删除商品 ---")

        try:
            goods_id = int(input("请输入要删除的商品编号："))
            goods = self.find_goods_by_id(goods_id)

            if goods:
                print(f"找到商品: {goods}")
                confirm = input("确认删除？(y/n)：")
                if confirm.lower() == 'y':
                    self.goods_list.remove(goods)
                    print(f"✓ 商品 '{goods.productName}' 已删除")
            else:
                print("商品不存在！")
        except ValueError:
            print("请输入有效的编号！")

    def modify_goods(self):
        """修改商品"""
        print("\n--- 修改商品 ---")

        try:
            goods_id = int(input("请输入要修改的商品编号："))
            goods = self.find_goods_by_id(goods_id)

            if not goods:
                print("商品不存在！")
                return

            print(f"当前商品信息: {goods}")
            print("=" * 30)

            # 修改价格
            try:
                new_price = input("请输入新价格 (直接回车跳过)：")
                if new_price:
                    if goods.set_price(float(new_price)):
                        print("价格已更新")
                    else:
                        print("价格无效！")
            except ValueError:
                print("价格格式错误！")

            # 修改库存
            try:
                new_stock = input("请输入新库存 (直接回车跳过)：")
                if new_stock:
                    goods.stock = int(new_stock)
                    print("库存已更新")
            except ValueError:
                print("库存格式错误！")

            # 修改类别
            new_category = input(f"请输入新类别 {Goods.get_categories()} (直接回车跳过)：")
            if new_category:
                goods.category = new_category

            print(f"✓ 商品信息已更新")

        except ValueError:
            print("输入错误！")

    def set_discount(self):
        """设置折扣"""
        print("\n--- 设置商品折扣 ---")

        try:
            goods_id = int(input("请输入商品编号："))
            goods = self.find_goods_by_id(goods_id)

            if not goods:
                print("商品不存在！")
                return

            print(f"当前商品: {goods.productName}, 原价: {Goods.format_currency(goods.productPrice)}")

            discount = float(input("请输入折扣 (0.1-1.0)："))
            if goods.set_discount(discount):
                print(f"✓ 折扣已设置，现价: {Goods.format_currency(goods.get_price())}")
            else:
                print("折扣设置失败！必须在0.1-1.0之间")

        except ValueError:
            print("输入错误！")

    def show_sales(self):
        """查看销售记录"""
        print("\n--- 销售记录 ---")

        sales = FileHandler.read_sales()

        if not sales:
            print("暂无销售记录")
            return

        print("编号\t商品名称\t单价\t数量\t总价")
        print("-" * 50)

        total_revenue = 0
        for sale in sales:
            total = sale['price'] * sale['quantity']
            total_revenue += total
            print(f"{sale['id']}\t{sale['name']}\t{sale['price']}\t{sale['quantity']}\t{Goods.format_currency(total)}")

        print("-" * 50)
        print(f"总收入: {Goods.format_currency(total_revenue)}")

    def generate_report(self):
        """生成销售报告"""
        print("\n" + "=" * 60)
        print("销售报告")
        print("=" * 60)

        # 商品统计
        print(f"商品总数: {Goods.get_total_goods()}")
        print(f"当前库存商品: {len(self.goods_list)}种")

        if self.goods_list:
            total_value = 0
            for g in self.goods_list:
                total_value += g.get_price() * g.stock
            print(f"库存总价值: {Goods.format_currency(total_value)}")

        # 类别统计
        categories = {}
        for goods in self.goods_list:
            cat = goods.category
            if cat in categories:
                categories[cat] += 1
            else:
                categories[cat] = 1

        print("\n类别分布:")
        for cat, count in categories.items():
            print(f"  {cat}: {count}种")

        # 销售统计
        sales = FileHandler.read_sales()
        if sales:
            total_sales = len(sales)
            total_revenue = 0
            for s in sales:
                total_revenue += s['price'] * s['quantity']

            print(f"\n总销售单数: {total_sales}")
            print(f"总销售额: {Goods.format_currency(total_revenue)}")

        print("=" * 60)

    def manage_staff(self):
        """管理员工"""
        print("\n--- 员工管理 ---")
        print("1. 查看所有员工")
        print("2. 添加员工")
        print("3. 删除员工")

        choice = input("请选择：")

        if choice == "1":
            print("\n员工列表:")
            for staff in self.staff_list:
                print(f"  {staff}")

        elif choice == "2":
            self.register()

        elif choice == "3":
            name = input("请输入要删除的员工用户名：")
            for staff in self.staff_list:
                if staff.name == name:
                    self.staff_list.remove(staff)
                    FileHandler.write_staff(self.staff_list)
                    print(f"员工 {name} 已删除")
                    return
            print("员工不存在！")


# ==================== controllers/user_controller.py ====================
class UserController:
    """用户控制器"""

    def __init__(self, goods_list, user_list, history_list):
        self.goods_list = goods_list
        self.user_list = user_list
        self.history_list = history_list
        self.current_user = None

    def login(self):
        """用户登录"""
        print("\n======= 用户登录 =======")

        for attempt in range(3):
            name = input("请输入账户名称：")
            password = input("请输入账户密码：")

            for user in self.user_list:
                if user.name == name and user.verify_login(password):
                    self.current_user = user
                    print("========= 登录成功 =========")
                    return True

            if attempt < 2:
                print(f"账户名称或密码错误，您还有 {2 - attempt} 次机会")

        print("========= 登录失败 =========")
        return False

    def register(self):
        """注册新用户"""
        print("\n======= 用户注册 =======")

        # 输入用户名
        while True:
            name = input("请输入新用户名称：")
            # 检查是否已存在
            exists = False
            for user in self.user_list:
                if user.name == name:
                    exists = True
                    break

            if not exists:
                break
            print("用户名已存在，请重新输入！")

        # 输入密码
        password = input("请输入密码：")
        repassword = input("请再次输入密码：")

        if password == repassword:
            new_user = User(name, password)
            self.user_list.append(new_user)
            FileHandler.write_users(self.user_list)
            print("****** 用户注册成功 ******")
            return True
        else:
            print("两次密码不一致，注册失败！")
            return False

    def show_menu(self):
        """显示用户菜单"""
        while True:
            print("\n" + "=" * 50)
            print(f"用户菜单 - 欢迎 {self.current_user.name}")
            print(f"积分: {self.current_user.points} | VIP等级: {self.current_user.vip_level}")
            print("=" * 50)
            print("1. 浏览商品")
            print("2. 搜索商品")
            print("3. 查看购物车")
            print("4. 添加商品到购物车")
            print("5. 结账")
            print("6. 查看购买历史")
            print("0. 退出")
            print("-" * 50)

            choice = input("请选择操作：")

            if choice == "1":
                self.show_all_goods()
            elif choice == "2":
                self.search_goods()
            elif choice == "3":
                self.view_cart()
            elif choice == "4":
                self.add_to_cart()
            elif choice == "5":
                self.checkout()
            elif choice == "6":
                self.view_history()
            elif choice == "0":
                break
            else:
                print("无效选择，请重新输入！")

    def show_all_goods(self):
        """显示所有商品"""
        print("\n" + "=" * 50)
        print("商品列表")
        print("=" * 50)
        print("编号\t商品名称\t价格\t库存")
        print("-" * 50)

        for goods in self.goods_list:
            print(goods)

        print("=" * 50)

    def search_goods(self):
        """搜索商品"""
        keyword = input("请输入商品名称关键字：")

        results = []
        for goods in self.goods_list:
            if keyword.lower() in goods.productName.lower():
                results.append(goods)

        if results:
            print(f"\n找到 {len(results)} 种商品:")
            for goods in results:
                print(goods)
        else:
            print("未找到相关商品")

    def find_goods_by_id(self, goods_id):
        """通过ID查找商品"""
        for goods in self.goods_list:
            if goods.id == goods_id:
                return goods
        return None

    def view_cart(self):
        """查看购物车"""
        print("\n" + "=" * 50)
        print(self.current_user.view_cart())
        print("=" * 50)

    def add_to_cart(self):
        """添加商品到购物车"""
        try:
            goods_id = int(input("请输入商品编号："))
            goods = self.find_goods_by_id(goods_id)

            if not goods:
                print("商品不存在！")
                return

            print(f"商品: {goods}")

            quantity = int(input("请输入数量："))
            if quantity <= 0:
                print("数量必须大于0！")
                return

            if quantity > goods.stock:
                print(f"库存不足！当前库存: {goods.stock}")
                return

            self.current_user.add_to_cart(goods, quantity)
            print(f"✓ 已添加到购物车")

        except ValueError:
            print("输入错误！")

    def checkout(self):
        """结账"""
        cart = self.current_user.cart

        if not cart:
            print("购物车是空的！")
            return

        print("\n" + "=" * 50)
        print("结账确认")
        print("=" * 50)
        print(self.current_user.view_cart())

        total = self.current_user.get_cart_total()

        # VIP折扣
        if self.current_user.vip_level > 0:
            discount = 1 - self.current_user.vip_level * 0.02
            final_total = total * discount
            print(f"VIP折扣: {int((1 - discount) * 100)}%")
            print(f"折后价: {Goods.format_currency(final_total)}")
        else:
            final_total = total

        confirm = input(f"总计 {Goods.format_currency(final_total)}，确认购买？(y/n)：")

        if confirm.lower() == 'y':
            # 更新库存和记录
            for goods, qty in cart:
                goods.reduce_stock(qty)

                # 记录历史
                history = History(goods.id, goods.productName, goods.get_price(), qty)
                self.history_list.append(history)

                # 记录销售
                FileHandler.record_sale(goods.id, goods.productName, goods.get_price(), qty)

            # 添加积分
            points_earned = int(final_total)
            self.current_user.add_points(points_earned)

            print(f"✓ 购买成功！获得 {points_earned} 积分")

            # 清空购物车
            self.current_user.clear_cart()

    def view_history(self):
        """查看购买历史"""
        if self.history_list:
            print("\n" + "=" * 50)
            print("购买历史")
            print("=" * 50)

            # 显示最近10条
            start = max(0, len(self.history_list) - 10)
            for i in range(start, len(self.history_list)):
                print(self.history_list[i])

            print("=" * 50)
        else:
            print("暂无购买历史")


# ==================== main.py ====================
def main():
    """主函数"""
    print("=" * 60)
    print("      ABC超市管理系统")
    print("=" * 60)

    # 初始化数据
    goods_list = FileHandler.read_goods()
    if not goods_list:
        # 如果没有数据，创建示例数据
        goods_list = [
            Goods(1, "苹果", 5.5, "食品"),
            Goods(2, "香蕉", 3.0, "食品"),
            Goods(3, "可乐", 4.5, "饮料"),
            Goods(4, "薯片", 6.0, "食品"),
            Goods(5, "纸巾", 12.0, "日用品")
        ]
        goods_list[0].stock = 50
        goods_list[1].stock = 30
        goods_list[2].stock = 20
        goods_list[3].stock = 15
        goods_list[4].stock = 40

    staff_list = FileHandler.read_staff()
    if not staff_list:
        staff_list = [
            Staff("admin", "admin123", "店长"),
            Staff("staff1", "pass123", "员工")
        ]

    user_list = FileHandler.read_users()
    if not user_list:
        user_list = [
            User("user1", "pass123"),
            User("vipuser", "vip123", 1)
        ]

    history_list = []

    # 主循环
    while True:
        print("\n" + "=" * 50)
        print("请选择登录身份：")
        print("1. 管理员")
        print("2. 普通用户")
        print("3. 注册新用户")
        print("0. 退出系统")
        print("-" * 50)

        choice = input("请输入选择：")

        if choice == "1":
            # 管理员登录
            controller = Manager(goods_list, staff_list)
            if controller.login():
                controller.show_menu()

        elif choice == "2":
            # 用户登录
            controller = UserController(goods_list, user_list, history_list)
            if controller.login():
                controller.show_menu()

        elif choice == "3":
            # 注册新用户
            controller = UserController(goods_list, user_list, history_list)
            if controller.register():
                print("注册成功，请登录")

        elif choice == "0":
            # 保存所有数据
            FileHandler.write_goods(goods_list)
            FileHandler.write_users(user_list)
            FileHandler.write_staff(staff_list)
            print("\n感谢使用，再见！")
            break

        else:
            print("无效选择，请重新输入！")


if __name__ == '__main__':
    main()
