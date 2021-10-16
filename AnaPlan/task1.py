def solution(A, X):
    N = len(A)
    if N == 0:
        return -1
    l = 0
    r = N - 1
    while l < r:
        m = (l + r + 1) // 2
        if A[m] > X:
            r = m - 1
        else:
            l = m
    if A[l] == X:
        return l
    return -1


res = solution([1, 2, 3, 4], 5)
print([1, 2, 3, 4], 5, res, sep='\n')
res = solution([1, 2, 3, 4, 5], 5)
print([1, 2, 3, 4, 5], 5, res, sep='\n')
res = solution([1, 2, 3, 4, 5, 6], 5)
print([1, 2, 3, 4, 5, 6], 5, res, sep='\n')
res = solution([1, 2, 3, 4, 5, 6], 1)
print([1, 2, 3, 4, 5, 6], 1, res, sep='\n')
res = solution([2, 3, 4, 5, 6], 1)
print([2, 3, 4, 5, 6], 1, res, sep='\n')
res = solution([1, 2, 3], 1)
print([1, 2, 3], 1, res, sep='\n')
res = solution([1, 2, 3, 4, 5, 6], 3)
print([1, 2, 3, 4, 5, 6], 3, res, sep='\n')
res = solution([1, 2, 4, 5, 6], 3)
print([1, 2, 4, 5, 6], 3, res, sep='\n')
res = solution([3], 3)
print([3], 3, res, sep='\n')
