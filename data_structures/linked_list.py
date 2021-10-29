from typing import Any, List


class ListNode:
    """
    Represents the node of the singly-linked list
    """
    def __init__(self, value, index=0, next=None):
        """
        Initialize the node
        :param value: value to be stored inside node
        :param index: represents the position in the linked list
        :param next: reference to the next element in the list
        """
        self.value = value
        self.index = index
        self.next = next

    def __str__(self):
        return f"{self.index}-{self.value}"

    def get_value(self):
        return self.value

    def get_index(self):
        return self.index

    def get_next(self):
        return self.next


class LinkedList:
    """
    Implementation of the singly-linked list

    Every node contains the reference to the next node in the list
    """
    def __init__(self):
        self.root = None
        self.sentinel = ListNode(None, -1, self.root)
        self.__size = 0

    def __str__(self):
        res = ""
        cur_node = self.root
        while cur_node is not None:
            res += " " + str(cur_node)
            cur_node = cur_node.next

        return res

    def size(self) -> int:
        return self.__size

    def add_all(self, values: List[int]):
        if values is None or len(values) == 0:
            raise Exception("list of values cannot be empty or None")
        for value in values:
            self.append(ListNode(value))

    def get_root(self) -> ListNode:
        """
        :return: root node of the linked list
        """
        return self.root

    def get_last_node(self) -> ListNode:
        """
        Find and return the last node in the linked list
        :return: last node in the linked list
        """
        cur_node = self.root
        if cur_node is None:
            return None
        while True:
            if cur_node.next is None:
                return cur_node
            cur_node = cur_node.next

    def append(self, new_node: ListNode):
        """
        Insert element to the end of the list
        :param new_node: node to be added to the end
        """
        last_node = self.get_last_node()
        if last_node is None:
            self.prepend(new_node)
        else:
            new_node.index = last_node.index + 1
            last_node.next = new_node
            self.__size += 1

    def prepend(self, new_node: ListNode):
        """
        Insert element at the beginning of the list
        :param new_node: node to be added at the beginning
        """
        new_node.next = self.root
        self.root = new_node
        self.sentinel.next = self.root
        LinkedList.__update_indexes(new_node, 0)
        self.__size += 1

    @staticmethod
    def __update_indexes(node: ListNode, start: int):
        cur_node = node
        while cur_node is not None:
            cur_node.index = start
            start += 1
            cur_node = cur_node.next

    def lookup(self, value: Any) -> int:
        """
        Find index of the element by value
        :param value: value to find
        :return: index of the element with the specified value. May return -1 if there are no such element
        """
        index = -1
        cur_node = self.root
        while cur_node is not None:
            if cur_node.value == value:
                index = cur_node.index
                break
            cur_node = cur_node.next
        return index

    def insert(self, node: ListNode, index: int):
        """
        Insert element into specific position with indexes right shift

        May raise ane exception if index is bigger than list size

        :param node: the node to be inserted
        :param index: insert position
        """

        if index >= self.__size:
            raise IndexError("Index is out of range")

        cur_node = self.root
        while cur_node.next is not None:
            if cur_node.next.index == index:
                node.next = cur_node.next
                cur_node.next = node
                LinkedList.__update_indexes(node, index)
                break
            cur_node = cur_node.next

        self.__size += 1
        pass

    def delete(self, index: int):
        """
        Delete an element in specific position

        May raise ane exception if index is bigger than list size
        :param index: index of the element to be removed
        """
        if index >= self.__size:
            raise IndexError("Index is out of range")

        if index == 0:
            self.root = self.root.next
            LinkedList.__update_indexes(self.root, index)
            self.__size -= 1
            return

        cur_node = self.root
        while cur_node.next is not None:
            if cur_node.next.index == index:
                cur_node.next = cur_node.next.next
                LinkedList.__update_indexes(cur_node.next, index)
                break
            cur_node = cur_node.next

        self.__size -= 1
