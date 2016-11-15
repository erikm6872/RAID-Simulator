# CSCI 460 Final Project
# RAID-5 Simulator
#
# Erik McLaughlin & Tyler Wright
# 11/14/2016
from Disk import Disk


def main():
    disks = [Disk(0), Disk(1), Disk(2)]
    data = "011010000110010101101100011011000110111100100000011101110110111101110010011011000110010000001010"
    write_string(data, disks)
    for x in disks:
        print(x)


def write_string(data, disks):
    i = 0
    for x in data:
        disks[i].write(x)
        i = (i + 1) % len(disks)
main()
