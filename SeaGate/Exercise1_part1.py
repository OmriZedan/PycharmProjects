__author__ = 'Omri Zedan'

"""
Problem:
Given a ladder with N steps, on which one is allowed to climb using one of the following:

A single step climb
2 steps climb 
implement a recursive function in python, that receives N and returns the number of legal ways to climb this ladder.

Climb(n) -> k

========================================================================================================================

Solution:
A backtracking recursive traversal solution is required here to go over all possible legal ways to arrive at the 
Nth step of the ladder.
 """


def climb(n: int) -> int:
    if n == 0:
        return 1
    elif n < 0:
        return 0

    return climb(n - 1) + climb(n - 2)


# ================================================== TESTING ===========================================================

def test_climb(n: int):
    k = climb(n)
    print(f"climb({n}) returns {k}")


test_climb(3)
test_climb(5)
test_climb(8)
test_climb(10)
test_climb(20)
