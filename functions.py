def intTOboolArr(num, size):
    bin_string = format(num, size)
    return [x == '1' for x in bin_string[::]]

def boolArrTOint(boolArr):
    w = 0
    for x in boolArr:
        w = w * 2 + int(x)
    return w

