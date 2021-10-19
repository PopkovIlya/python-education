"""This module allows you to use binary sort, quick sort and find factorial of numbers.

This module imports the 'typing' and the 'collection' package from the standard library.

This file can also be imported as a module and contains the following
classes:
    *Algo
        Contains implementation of the most common algorithms
     Methods
     -------
     binary_search(arr: List[int], target: int) -> int : staticmethod
        Binary search implementation, allows you to find the index
        of an element in a sorted array.
    factorial(n_mult: int) -> int : staticmethod
        Factorial implementation with recursive approach.
    quick_sort(start: int, end: int, arr: List[int]) : staticmethod
        Quick sort implementation, sorts an array in natural order.

"""

from typing import List
from collections import deque


class Algo:
    """Contains implementation of binary sort, quick sort,
     and finding the factorial of numbers.

     Methods
     -------
     binary_search(arr: List[int], target: int) -> int : staticmethod
        Binary search implementation, allows you to find the index
        of an element in a sorted array.
    factorial(n_mult: int) -> int : staticmethod
        Factorial implementation with recursive approach.
    quick_sort(start: int, end: int, arr: List[int]) : staticmethod
        Quick sort implementation, sorts an array in natural order.

     """

    @staticmethod
    def binary_search(arr: List[int], target: int) -> int:
        """
        Binary search implementation, allows you to find the index
        of an element in a sorted array
        :parameter arr - array of ints. Array should be sorted or else result
            is not guaranteed
        :parameter target - the number which we are looking inside the array
        :returns the index of the target or -1 if it is not found
        """

        if not arr or len(arr) == 0:
            return -1

        left, right = 0, len(arr)-1

        while left < right:
            mid = left + (right - left)//2

            if arr[mid] >= target:
                right = mid
            else:
                left = mid+1

        return left if arr[left] == target else -1

    @staticmethod
    def factorial(n_mult: int) -> int:
        """Factorial implementation with recursive approach
        :parameter n_mult - integer. Shows how many times we will do the multiplication
        :returns the multiplication of all numbers starting from 0 to n. If n == 0,
        function returns 1.
        """

        if n_mult in (0, 1):
            return 1

        return n_mult * Algo.factorial(n_mult - 1)

    @staticmethod
    def quick_sort(arr: list):
        """Quick sort (iterative) implementation
            It sorts an array in natural order
            :parameter arr - array of numbers
        """
        if len(arr) == 0:
            return []
        if len(arr) == 1:
            return arr
        stack = deque()
        start = 0
        end = len(arr) - 1
        stack.append((start, end))

        while stack:
            start, end = stack.pop()
            pivot = Algo.__partition(arr, start, end)
            if pivot - 1 > start:
                stack.append((start, pivot - 1))
            if pivot + 1 < end:
                stack.append((pivot + 1, end))

    @staticmethod
    def __partition(arr: list, start: int, end: int):
        pivot = arr[end]
        p_index = start

        for i in range(start, end):
            if arr[i] <= pivot:
                arr[i], arr[p_index] = arr[p_index], arr[i]
                p_index = p_index + 1
        arr[p_index], arr[end] = arr[end], arr[p_index]
        return p_index


if __name__ == '__main__':
    sorted_arr = [-10, -3, 0, 1, 7, 90, 150, 333]
    print(Algo.binary_search(sorted_arr, 90))

    print(Algo.factorial(5))

    arr1 = [9, -3.5, 5.2, 2.3, 6, 8, -6, 1, 3]
    Algo.quick_sort(arr1)
    print(arr1)
