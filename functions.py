def intTOboolArr(num, size):
    bin_string = format(num, size)
    return [x == '1' for x in bin_string[::]]

def boolArrTOint(boolArr):
    w = 0
    for x in boolArr:
        w = w * 2 + int(x)
    return w

#Additional function (not used) for understanding of binary conversion
def binarytoint(b):
    w=0
    string = b
    for x in string:
        w = w*2+x
    return w

def boolList2BinString(lst):
    return '0b' + ''.join(['1' if x else '0' for x in lst])


