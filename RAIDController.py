# CSCI 460 Final Project
# RAID-5 Simulator
#   RAIDController.py
# Erik McLaughlin & Tyler Wright
# 11/14/2016
from Disk import Disk


def split_data(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]


class RAIDController:

    disks = []

    def __init__(self, num_disks):
        for i in range(num_disks):
            self.disks.append(Disk(i))

    # Writes a string of bits to the RAID disks
    def write_string(self, data):
        blocks = split_data(data, len(self.disks)-1)
        parity_disk = len(self.disks) - 1   # Starts at the last disk and moves backwards

        for x in blocks:
            # Calculate parity bit for block x
            parity_bit = None
            for b in x:
                parity_bit = parity_bit ^ b if parity_bit is not None else b

            # Insert the parity bit into the block at the position of the current parity disk
            x.insert(parity_disk, parity_bit)

            # Calculate the new parity disk
            if parity_disk == 0:
                parity_disk = len(self.disks) - 1
            else:
                parity_disk -= 1

            # Write block to disks
            for i in range(len(self.disks)):
                self.disks[i].write(x[i])

    # Simulate a disk failing by removing it from the list
    def disk_fails(self, disk_num):
        del self.disks[disk_num]

    def print_data(self):
        for x in self.disks:
            print(x)
