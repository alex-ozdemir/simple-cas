from system import *


def main():
    while True:
        system = System()
        system.editEquations()
        system.use()
        user_input = raw_input("Type 'new' to continue.\nType anything else to quit.")
        if user_input != 'new':
            break
    print "Goodbye"
    i = raw_input()

if __name__ == '__main__':
    main()
