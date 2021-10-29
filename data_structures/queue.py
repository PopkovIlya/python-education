from typing import Any

from linked_list import ListNode
from linked_list import LinkedList


class Queue:
    """
    Queue implementation using LinkedList under the hood
    """

    def __init__(self):
        self.ll = LinkedList()

    def enqueue(self, elem: Any):
        """
        add element at the end of the queue
        """
        self.ll.append(ListNode(elem))

    def dequeue(self) -> Any:
        """
        get and remove the element from the beginning of the queue
        :return: element value or None if queue is empty
        """
        if self.ll.size() == 0:
            return None
        elem = self.ll.get_root()
        self.ll.delete(0)
        return elem.value

    def peek(self) -> Any:
        """
        get the value of the first element in the queue
        :return: element value or None if queue is empty
        """
        if self.ll.size() == 0:
            return None
        return self.ll.get_root().value

    def size(self):
        return self.ll.size()
