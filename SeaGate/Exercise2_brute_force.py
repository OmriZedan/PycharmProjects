__author__ = 'Omri Zedan'

from typing import Tuple

"""
Problem:
Given an list of integers of the size of N, 
you need to return (start_index, end_index) to designate the subarray with the highest sum.

Simple solution O(N^2):
Go over all possible sub-arrays using a nested loop, and pick one with the highest possible sum. 
"""


def find_sub_array_with_largest_sum(array: list) -> Tuple[int, int]:
    start = 0
    end = 0
    max_sum = array[0]

    for current_start in range(len(array) - 1):
        for current_end in range(current_start + 1, len(array) + 1):
            current_sum = sum(array[current_start: current_end])
            if current_sum > max_sum:
                max_sum = current_sum
                start = current_start
                end = current_end

    return start, end - 1


# ================================================== TESTING ===========================================================

def test_find_sub_array_with_largest_sum(array: list):
    start, end = find_sub_array_with_largest_sum(array)
    print(f"The the highest is confined within: ({start},{end})")


test_find_sub_array_with_largest_sum([0, 10, 20, -647, 10, 4, 20])
test_find_sub_array_with_largest_sum([1, 1, 1, 1, 1, 1, 1, 1])
