def Q1(a, b, c):
    def f(x):
        return 2 * x + 1

    def g(x):
        return x + 7

    sum = 0
    for x in range(a, b + 1):
        if x == c:
            continue
        if x % 2 == 0:
            sum += f(x)
        else:
            sum += g(x)

    return sum


print(Q1(a=1, c=2, b=7))
