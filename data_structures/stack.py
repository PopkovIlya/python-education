from linked_list import *


class Stack:
    """
    Stack implementation based on the custom LinkedList
    """

    def __init__(self):
        self.ll = LinkedList()

    def push(self, elem: Any) -> None:
        """
        add the element to the stack
        :param elem: value to be added into stack
        """
        self.ll.append(ListNode(elem))

    def pop(self) -> Any:
        """
        get and remove the last element of the stack
        :return: the value of the last element of the stack or None if stack is empty
        """
        if self.ll.size() == 0:
            return None
        last_elem = self.ll.get_last_node()
        self.ll.delete(last_elem.index)
        return last_elem.value

    def peek(self) -> Any:
        """
        get the value of the last element in the stack
        :return: element value or None if stack is empty
        """
        if self.ll.size() == 0:
            return None
        return self.ll.get_last_node().value

    def size(self) -> int:
        return self.ll.size()
