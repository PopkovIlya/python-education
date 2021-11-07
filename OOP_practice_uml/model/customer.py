import random

from model.menu import Menu
from model.order import Order, Bill, OrderType
from model.kitchen import Dish


class Customer:
    """
    Customer representation
    """

    def __init__(self, cid: int, first_name: str, last_name: str, money: int):
        self.cid = cid
        self.first_name = first_name
        self.last_name = last_name
        self.money = money
        self.order_type = None

    def make_order(self, menu: Menu) -> Order:
        """
        Making order based on the restaurant's menu

        :param menu: the restaurant's menu
        :return: the order
        """
        menu_items = menu.get_items()
        order = Order(self.order_type, self.cid)
        total_sum = 0
        for i in range(3):
            item = random.choice(menu_items)
            if total_sum + item.price < self.money:
                total_sum += item.price
                order.add_item(item, 1)
        print(f"{self.first_name} {self.last_name} ordered:")
        print(order)
        return order

    def consume(self, dish: Dish):
        """
        Consume the dish

        :param dish: a dish to be consumed
        """
        print(f"eating {dish.name}")

    def pay(self, bill: Bill) -> int:
        """
        Paying for a bill

        :param bill: the bill
        :return: amount of money to be payed
        """
        return 0


class Visitor(Customer):
    """
    An offline visitor implementation for the customer.

    He should visit the restaurant himself
    """

    def __init__(self, cid: int, first_name: str, last_name: str, money: int):
        super().__init__(cid, first_name, last_name, money)
        self.order_type = OrderType.local

    def call_waiter(self):
        """
        Call the waiter
        """
        print("Hey, you!")

    def pay(self, bill: Bill) -> int:
        print("paying cash")
        price = bill.get_total_price()
        self.money -= price
        return price


class OnlineCustomer(Customer):
    """
    The online visitor.

    He should not attend the restaurant, but can make an order online
    """

    def __init__(self, cid: int, first_name: str, last_name: str, money: int):
        super().__init__(cid, first_name, last_name, money)
        self.order_type = OrderType.online

    def pay(self, bill: Bill) -> int:
        print("paying online")
        price = bill.get_total_price()
        self.money -= price
        return price

