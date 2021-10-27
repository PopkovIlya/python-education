import random

import pytest

from hw10_algo import Algo


class TestBinarySearch:
    def test_binary_search(self):
        arr = [1, 2, 3, 4, 5, 6, 7]
        target = 6
        expected_result = 5
        result = Algo.binary_search(arr, target)
        assert result == expected_result

    @pytest.mark.parametrize(
        "arr, target, expected_result",
        [(None, 1, -1), ([], 1, -1),
         ([i for i in range(1000)], 500, 500),
         ([i for i in range(1000)], 1000, -1)]
    )
    def test_binary_search_to_return_negative_number(self, arr, target, expected_result):
        result = Algo.binary_search(arr, target)
        assert result == expected_result

    def test_return_negative_number_if_target_not_found(self):
        arr = [1, 2, 3, 4, 5]
        target = 6
        expected_result = -1
        result = Algo.binary_search(arr, target)
        assert result == expected_result


@pytest.mark.parametrize("number, expected_result",
                         [(0, 1), (1, 1), (2, 2), (3, 6), (4, 24)])
def test_factorial(number, expected_result):
    result = Algo.factorial(number)
    assert result == expected_result


class TestQuickSort:

    def test_quick_sort(self):
        arr = [10, 7, 8, 9, 1, 5]
        expected_result = [1, 5, 7, 8, 9, 10]

        Algo.quick_sort(arr)
        assert arr == expected_result

    @pytest.mark.parametrize(
        "arr",
        [[], [1], random.sample(range(-1000, 0), k=8),
         random.sample(range(1000), k=8),
         random.sample(range(-1000, 1000), k=100)])
    def test_quick_sort_with_negative_numbers(self, arr):
        start_arr = arr[:]
        sorted_arr = sorted(arr)
        Algo.quick_sort(start_arr)
        assert start_arr == sorted_arr
