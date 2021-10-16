def Q6(list_of_strings: list):
    def f1(string1):
        count = 0
        for c in string1:
            if c == 'z':
                count += 1

        return count

    def f2(string2):
        count = 0
        for c in string2:
            if c == "p":
                count +=1
        return count

    def f3(string3):
        return len(string3) * 2

    sum = 0
    for string in list_of_strings:
        c = string[0]
        if c in "abcdefg":
            sum += f1(string1=string)
        elif c in "hijklmn":
            sum += f2(string2=string)
        elif c in "opqrstuvwxyz":
            sum += f3(string3=string)

    print("Total points = " + str(sum))


list_of_strings = [
    "azz",  # 2
    "zc",   # 4
    "ippp", # 3
    "zab",  # 6
    "uvxz"  # 8
]
Q6(list_of_strings=list_of_strings)
