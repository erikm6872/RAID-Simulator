# CSCI 460 Final Project
# RAID-5 Simulator
#
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016

from RAIDController import *

data = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'# Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'


def main():
    controller = RAIDController(4)
    controller.write_string(convert_string(data))
    controller.print_data()

    orig_disks = list(controller.disks)

    controller.disk_fails(3)
    controller.reconstruct_disk(3)
    controller.print_data()

    try:
        controller.validate_disks(orig_disks)
    except DiskReconstructException as e:
        print(e.msg)

    print("Original: " + data)
    print("Read:     " + controller.read_all())

    if data != controller.read_all():
        print("R/W Error: Strings are different")


def convert_string(d):
    bin_list = []
    for x in d:
        bin_list.append(format(ord(x), '#010b'))   # Change character -> integer -> binary string and append to list
    return bin_list

main()
