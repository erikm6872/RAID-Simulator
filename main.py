# CSCI 460 Final Project
# RAID-5 Simulator
#
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016

from RAIDController import *

data = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'#Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'


def main():
    controller = RAIDController(5)
    d = ''.join(format(ord(x), 'b') for x in data)[2:]
    controller.write_string(convert_string(d))
    controller.print_data()

    # controller.disk_fails(1)
    # controller.print_data()

    print("Original: " + d)
    print("Read:     " + controller.read_all())

    if d != controller.read_all():
        print("R/W Error: Strings are different")


def convert_string(d):
    bin_list = []
    for x in d:
        bin_list.append(int(x))
    return bin_list

main()
