__author__ = 'Omri Zedan'

"""
This is an enhancement to Exercise 1 Part 1 solution as described in Part 3.
The enhancement introduces the use of a key-value structure to cut down recurring calculations. 
 """

climb_results = dict()


def climb(n: int) -> int:
    if n == 0:
        return 1
    elif n < 0:
        return 0

    climb_results[n - 1] = climb_results.get(n - 1, climb(n - 1))
    climb_results[n - 2] = climb_results.get(n - 2, climb(n - 2))

    return climb_results[n - 1] + climb_results[n - 2]


# ================================================== TESTING ===========================================================

def test_climb(n: int):
    k = climb(n)
    print(f"climb({n}) returns {k}")


test_climb(3)
test_climb(5)
test_climb(8)
test_climb(10)
test_climb(20)
