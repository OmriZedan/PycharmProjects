def Q4(string1, string2):
    string3 = ""
    remainder = ""

    if len(string1) > len(string2):
        remainder = string1[len(string2):]
    elif len(string2) > len(string1):
        remainder = string2[len(string1):]

    for c1, c2 in zip(string1, string2):
        string3 += c1
        string3 += c2

    string3 += remainder

    return string3
