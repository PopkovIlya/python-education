from time import sleep

from model.order import Order, Bill
from model.menu import Menu, Item
from model.kitchen import Dish, Kitchen
from model.customer import Customer


class Worker:
    """
    A worker interface. All workers types should implement it
    """
    pass


class Chief(Worker):
    """
    Master chief on the kitchen.
    He is responsible for cooking
    """

    def __init__(self, kitchen: Kitchen):
        self.kitchen = kitchen

    def cook(self, order: Order):
        """
        Prepare the dish based on the order.
        When dish is ready, it will be put into the kitchen's dish queue

        :param order: the order
        """
        for item in order.get_order().items():
            for i in range(item[1]):
                dish = self.__cook_dish(item[0], order)
                print(f"{dish.name} is ready")
                self.kitchen.add_ready_dish(dish)

    def __cook_dish(self, item: Item, order: Order) -> Dish:
        print(f"Cooking {item.name}...")
        sleep(1)
        return Dish(item.name, order)


class Waiter(Worker):
    """
    Working with customers, serve them by supplying them with food and drink as requested
    """

    def __init__(self, kitchen: Kitchen):
        super().__init__()
        self.kitchen = kitchen

    def receive_order(self, order: Order):
        """
        Receive an order from the customer and transfer it to the kitchen

        :param order: the order
        """
        self.kitchen.add_order(order)

    def bring_menu(self) -> Menu:
        """
        Brings the Menu to the Customer

        :return: the menu
        """
        return self.kitchen.get_menu()

    def deliver_order(self, order: Order, customer: Customer) -> int:
        """
        Deliver an order to the customer

        :param order: the order
        :param customer: the customer who needs an order
        """
        print(f"bringing order for {customer.first_name} {customer.last_name}")
        order_price = Bill(order).get_total_price()
        return order_price


class Courier(Worker):

    def deliver_order(self, order: Order, customer: Customer) -> int:
        """
        Deliver an order to the customer

        :param order: the order
        :param customer: the customer who needs an order
        """
        print(f"delivering order for {customer.first_name} {customer.last_name}")
        order_price = Bill(order).get_total_price()
        return order_price
