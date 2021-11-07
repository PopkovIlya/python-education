from typing import List


class Item:
    """
    Menu Item implementation
    """

    def __init__(self, name: str, description: str, price: int):
        self.name = name
        self.description = description
        self.price = price

    def __str__(self):
        return f"name: {self.name}; price: {self.price}"


class Menu:
    """
    Restaurant menu implementation
    """

    def __init__(self, items: List[Item]):
        self.__items = items

    def get_items(self) -> List[Item]:
        """
        :return: menu items
        """
        return self.__items
