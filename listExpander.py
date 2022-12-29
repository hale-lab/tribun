import math

def listExpander(list):
    total = 1.00
    new_list = []

    for i in range(len(list)):
        sum = math.fsum(list[:i+1])
        print(sum)
        if sum <= total:
            new_list.append(sum)

    return new_list

output_ = (listExpander(_input))