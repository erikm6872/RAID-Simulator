# CSCI 460 Final Project
# RAID-5 Simulator
#   RAIDController.py
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016
from Disk import Disk


def split_data(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]


class RAIDController:

    disks = []

    def __init__(self, num_disks):
        self.num_disks = num_disks
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
            parity_disk = parity_disk - 1 if parity_disk != 0 else len(self.disks) - 1

            # Write block to disks
            for i in range(len(x)):
                self.disks[i].write(x[i])

    # Read all data on disks, ignoring parity bits. Does not account for missing disks.
    def read_all(self):
        ret_str = ''
        parity_disk = len(self.disks) - 1  # Starts at the last disk and moves backwards
        for i in range(len(self.disks[0])):
            for j in range(self.num_disks):
                if j != parity_disk and i < len(self.disks[j]):
                    # Add bit to return string
                    ret_str += str(self.disks[j].read(i))
            # Update parity disk index
            parity_disk = parity_disk - 1 if parity_disk != 0 else len(self.disks) - 1
        return ret_str

    # Simulate a disk failing by removing it from the list
    def disk_fails(self, disk_num):
        print("Disk " + repr(disk_num) + " failed")
        del self.disks[disk_num]

    # Prints the data on each disk in a table. Parity bits are marked with '*'
    def print_data(self):
        for x in self.disks:
            print(" |  " + repr(x.disk_id), end="")
        print(" |")
        print(" --------------------------")

        parity_disk = len(self.disks) - 1  # Starts at the last disk and moves backwards
        for i in range(len(self.disks[0])):
            for j in range(len(self.disks)):
                if i < len(self.disks[j]):
                    print(" | " + repr(self.disks[j].read(i)), end="")
                    if j == parity_disk:
                        print("*", end="")
                    else:
                        print(" ", end="")
            parity_disk = parity_disk - 1 if parity_disk != 0 else len(self.disks) - 1
            print(" |")



