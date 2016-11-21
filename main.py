# CSCI 460 Final Project
# RAID-5 Simulator
#
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016
from argparse import *
from RAIDController import *


def main():
    parser = ArgumentParser(description='RAID-5 Simulator')
    parser.add_argument('-n', '--numdisks',
                        type=int,
                        default=4,
                        metavar='DISKS',
                        help='Number of disks in the RAID array. Default=4')

    parser.add_argument('-d', '--data',
                        type=str,
                        default='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor'
                                ' incididunt ut labore et dolore magna aliqua.Ut enim ad minim veniam, quis nostrud '
                                'exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
                        help='Data string to write to the disks array. Default is a Lorem Ipsum string.')

    args = parser.parse_args()
    num_disks = args.numdisks
    data = args.data

    if num_disks < 3:
        parser.error("RAID-5 requires a minimum of 3 disks.")

    controller = RAIDController(num_disks)
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
