__author__ = 'Omri Zedan'

import sys
from typing import Tuple

"""
Problem:
Given an list of integers of the size of N, 
you need to return (start_index, end_index) to designate the subarray with the highest sum.

Efficient solution O(N) - Kadane's Algorithm:
Go over the elements in a given array (in a sequential manner). 
Check per each element if the 'maximal' sum up to it (including the element) is larger that the element itself.  
If so, add it to the maximal sub-array. Else start a new maximal sub array starting from it.
"""

max_sub_array = dict(
    start=0,
    end=0,
    sum=-sys.maxsize
)
cur_sub_array = dict(
    start=0,
    end=0,
    sum=-sys.maxsize
)


def initialize_helper_structs():
    """
    initialize helper dictionaries to pre-run values.
    """
    for sub_array in cur_sub_array, max_sub_array:
        sub_array['start'] = 0
        sub_array['end'] = 0
        sub_array['sum'] = -sys.maxsize


def update_max_sub_array():
    update_sub_array(max_sub_array, cur_sub_array['start'], cur_sub_array['end'], cur_sub_array['sum'])


def update_cur_sub_array(start=None, end=None, cur_sum=None):
    update_sub_array(cur_sub_array, start, end, cur_sum)


def update_sub_array(sub_arr, start=None, end=None, new_sum=None):
    if start:
        sub_arr['start'] = start
    if end:
        sub_arr['end'] = end
    if new_sum:
        sub_arr['sum'] = new_sum


def find_sub_array_with_largest_sum(array: list) -> Tuple[int, int]:
    initialize_helper_structs()
    for i, v in enumerate(array):
        if v > cur_sub_array['sum'] + v:  # Should I start a new sub array ?
            #   YES
            cur_sum = v
            update_cur_sub_array(start=i, end=i, cur_sum=cur_sum)
        else:
            #   NO
            cur_sum = cur_sub_array['sum'] + v
            update_cur_sub_array(end=i, cur_sum=cur_sum)

        if cur_sum > max_sub_array['sum']:  # Should I update the max sum ?
            #   YES
            update_max_sub_array()

    return max_sub_array['start'], max_sub_array['end']


# ================================================== TESTING ===========================================================


def test_find_sub_array_with_largest_sum(array: list):
    start, end = find_sub_array_with_largest_sum(array)
    print(f"The the highest is confined within: ({start},{end})")


test_find_sub_array_with_largest_sum([0, 10, 20, -647, 10, 4, 20])
test_find_sub_array_with_largest_sum([1, 1, 1, 1, 1, 1, 1, 1])
