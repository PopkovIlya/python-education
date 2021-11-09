from collections import deque

from model.menu import Menu, Item
from model.order import Order


class Dish:
    """
    A dish which is ready to be consumed
    """

    def __init__(self, name: str, order: Order):
        self.name = name
        self.order = order


class Kitchen:
    """
    Restaurant's kitchen representation
    """

    def __init__(self):
        self.__menu = Kitchen.prepare_menu()
        self.__order_queue = deque()
        self.__ready_dishes = deque()

    @staticmethod
    def prepare_menu() -> Menu:
        """
        Prepares a menu for the restaurant

        :return: the menu
        """
        items = [Item("borsch", "very tasty soup", 20),
                 Item("grechka with mushrooms", "vegan garnier", 15),
                 Item("pasta", "Italian food", 12),
                 Item("icecream", "cold as my ex", 10),
                 Item("tea", "English breakfast", 5),
                 Item("coffee", "filter from the big can", 5)]
        menu = Menu(items)
        return menu

    def get_menu(self) -> Menu:
        """
        Returns the menu

        :return: the menu
        """
        return self.__menu

    def add_order(self, order: Order):
        """
        Adds a new order to the orders queue

        :param order: a new order
        """

        self.__order_queue.append(order)

    def get_orders(self):
        """
        :return: the orders queue
        """
        return self.__order_queue

    def get_next_order(self):
        """
        Get and remove the next order from the queue

        :return: the next order in the queue
        """
        return self.__order_queue.popleft()

    def add_ready_dish(self, dish: Dish):
        """
        Add the ready dish into the dishes queue

        :param dish: a new dish
        """

        self.__ready_dishes.append(dish)

    def get_dishes(self):
        """
        :return: the dishes queue
        """

        return self.__ready_dishes
