# CSCI 460 Final Project
# RAID-5 Simulator
#
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016
import sys
from argparse import *
from RAIDController import *
from RAID0_Controller import *
from RAIDFile import *
from RAIDExceptions import *

files = []


def main():
    parser = ArgumentParser(description='RAID-5 Simulator')
    parser.add_argument('-n', '--numdisks',
                        type=int,
                        default=5,
                        metavar='DISKS',
                        help='Number of disks in the RAID array. Default=5')

    parser.add_argument('-l', '--level',
                        type=int,
                        default=5,
                        choices=range(0,6),
                        help='RAID level to simulate. Default=5')

    parser.add_argument('-c', '--capacity',
                        type=int,
                        default=0,
                        metavar='CAP',
                        help='Storage capacity of each disk in bytes. Default=0 (unlimited)')

    parser.add_argument('-f', '--fail',
                        type=int,
                        default=2,
                        metavar='DISK',
                        help='Disk number to fail. Default=2')

    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='Fail each disk in sequence.')

    parser.add_argument('-d', '--data',
                        type=str,
                        nargs='*',
                        default=[
                            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt'
                            ' ut labore et dolore magna aliqua.',

                            'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea'
                            ' commodo consequat.',

                            'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat'
                            ' nulla pariatur.',

                            'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit'
                            ' anim id est laborum.'],
                        help='Data strings to write to the disks array. Default is a series of Lorem Ipsum strings.')
    
    parser.add_argument('-p', '--pause',
                        action='store_true',
                        help='Pause script between major actions. Used for demo purposes.')

    args = parser.parse_args()
    num_disks = args.numdisks
    disk_cap = args.capacity
    data = args.data

    if num_disks < 3:
        parser.error("RAID-5 requires a minimum of 3 disks.")
    if disk_cap < 0:
        parser.error("Disk capacity cannot be less than 0 bytes.")
    if args.fail >= num_disks:
        parser.error("Cannot fail disk " + repr(args.fail) + ": Invalid disk number")

    controller = RAID0_Controller(num_disks, disk_cap)

    for i in range(len(data)):
        f = RAIDFile(i, data[i])
        files.append(f)
        try:
            controller.write_file(f)
        except DiskFullException as e:
            controller.print_data()
            sys.exit(e.msg)
    
    controller.print_data()
    print(controller.read_all_data())
    
    if args.pause:
        input("Press enter to continue...")

    orig_disks = list(controller.disks)

    if args.all:
        fail_disks(range(num_disks), controller, orig_disks, args.pause)
    else:
        fail_disks([args.fail], controller, orig_disks, args.pause)

    print(controller.read_all_data())
    read_files = controller.read_all_files()
    if files != read_files:
        raise DataMismatchException(
            "Original and read strings are different.\nOriginal: " + repr(files) + "\nRead:     " + repr(read_files))


def fail_disks(disks, controller, orig_disks, pause=False):
    for x in disks:
        controller.disk_fails(x)
        controller.print_data()
        print(controller.read_all_data())
        if pause:
            input("Press enter to continue...")
        controller.reconstruct_disk(x)
        controller.print_data()
        try:
            controller.validate_disks(orig_disks)
        except DiskReconstructException as e:
            print(e.msg)

main()
