# CSCI 460 Final Project
# RAID-5 Simulator
#
# Erik McLaughlin & Tyler Wright
# 11/14/2016
from Disk import Disk


def main():
    d0 = Disk(0)
    d1 = Disk(1)
    d2 = Disk(2)

    d0.write("Disk 0")
    d1.write("Disk 1")
    d2.write("Disk 2")

    print(d0)
    print(d1)
    print(d2)
main()
