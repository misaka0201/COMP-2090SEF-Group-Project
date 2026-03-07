# COMP-2090SEF-Group-Project Task 1 
Chen Man Ho 14257154
##  Application: online shopping system
1. Class: Product is a class, and Product(1, "Apple", 5.5) creates a specific product object. The code defines multiple classes like Product, User, Staff
2. Inheritance: Person, Staff and User
Both Staff and User automatically possess the "name" and "password" attributes of the Person class.
3. Encapsulation: in the Product class, the stock attribute cannot be modified directly from outside. It must be changed through methods like add_stock() (for restocking) or sell() (for selling).
4. Polymorphism: __str__ method behaves in Product class: displays product information.
In User class: shows only the username.
In Staff class: shows name and staff ID.
Although the method name is the same, each class implements it in its own way.
5. Class Method: marked with @classmethod. For example, Product.get_total() can be called directly through the class name without creating an object, to get the total number of product types
6. Static Method: marked with @staticmethod. For example, Product.to_money() is a utility function that converts numbers to currency format.
7. Composition: the User class has a self.cart list that stores tuples of Product objects and their quantities.
`The language of the program output is only CHINESE`
