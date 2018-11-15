# Docs: https://pymotw.com/2/socket/tcp.html
from bitset import Bitset

def binarytoint(b):
    w=0
    string = b
    for x in string:
        w = w*2+x
    return w


def User():
    print("I'm User!")
    b = Bitset(7)
    print(b)
    print(binarytoint(b))
def Server():
    print("I'm Server!")

def menu():
    loop = 1
    start = 0
    while loop == 1:
        start = input("Choose working mode (Server-1, User-2, Exit-0):")
        if start == 1:
            Server()
            loop = 0
        elif start == 2:
            User()
            loop = 0
        elif start == 0:
            loop = 0
        else:
            print("Wrong choice. Choose again (type 1 for \"Server\" or 2 for \"User\" or 0 for Exit)")

menu()