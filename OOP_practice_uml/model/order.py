import enum
from typing import Dict
from model.menu import Item


class OrderType(enum.Enum):
    """
    Type of the order. Possible values: online, local
    """

    online = "online"
    local = "local"


class Order:
    """
    An order implementation
    """

    def __init__(self, order_type: OrderType, customer_id: int):
        self.__order = {}
        self.__order_type = order_type
        self.__customer_id = customer_id

    def __str__(self):
        res = ""
        for item in self.__order.items():
            res += str(item[0]) + " count: " + str(item[1]) + "\n"
        return res

    def add_item(self, item: Item, count: int):
        """
        Add a new item into the order

        :param item: an item to be added
        :param count: number of items to be added
        """
        self.__order[item] = count

    def get_order(self) -> Dict[Item, int]:
        """
        :return: the disc with ordered items
        """
        return self.__order

    def get_customer_id(self) -> int:
        """
        :return: customer ID
        """
        return self.__customer_id

    def get_order_type(self) -> OrderType:
        """
        :return: order type
        """
        return self.__order_type


class Bill:
    """
    Bill implementation.
    """

    def __init__(self, order: Order):
        self.__order = order

    def get_total_price(self) -> int:
        """
        Calculate total price based on the order

        :return: amount of money to be payed
        """
        total_price = 0
        for entry in self.__order.get_order().items():
            total_price += entry[0].price * entry[1]

        return total_price
