# CSCI 460 Final Project
# RAID-5 Simulator
#
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016

from RAIDController import *
from RAID_File import *
from RAIDExceptions import *

data = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
        'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.']
files = []


def main():
    controller = RAIDController(5)

    for i in range(len(data)):
        f = RAIDFile(i, data[i])
        files.append(f)
        controller.write_file(f)

    controller.print_data()

    orig_disks = list(controller.disks)

    for i in range(5):
        controller.disk_fails(i)
        controller.reconstruct_disk(i)
        controller.print_data()
        try:
            controller.validate_disks(orig_disks)
        except DiskReconstructException as e:
            print(e.msg)

    all_data = ""
    for x in data:
        all_data += x

    if all_data != controller.read_all():
        raise DataMismatchException("Original and read strings are different.\nOriginal: " + all_data + "\nRead:     " + controller.read_all())


main()
