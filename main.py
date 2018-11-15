def menu():
    loop = 1
    start = 0
    while loop == 1:
        start = input("Choose working mode (Server-1, User-2, Exit-0):")
        if start == 1:
            print()
        elif start == 2:
            print()
        elif start == 0:
            return 0
        else:
            print("Wrong choose. Choose again (type 1 for \"Server\" or 2 for \"User\" or 0 for Exit)")

menu()