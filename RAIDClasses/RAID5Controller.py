# CSCI 460 Final Project
# RAID-5 Simulator
#   RAIDController.py
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016

from colorama import Fore, Back, Style
from colorama import init

from RAIDExceptions import *
from RAIDClasses.RAIDController import *

init()

'''
RAID-5: Data is striped across n-1 disks, with parity calculations for each block. Parity bits are striped across disks.
'''


class RAID5Controller(RAIDController):
    __metaclass__ = RAIDController

    # Writes a string of bits to the RAID disks
    def write_bits(self, data):
        blocks = split_data(data, len(self.disks)-1)

        for x in blocks:
            # Calculate parity bit for block x. We need to convert the bin strings to integers in order to use bit
            # manipulation to calculate the XOR

            parity_bit = self.calculate_parity(x)
            self.validate_parity(x + [format(parity_bit, bin_format)])

            parity_disk = self.calculate_parity_disk(len(self))

            # Insert the parity bit into the block at the position of the current parity disk
            x.insert(parity_disk, format(parity_bit, bin_format))

            # Write block to disks
            for i in range(len(x)):
                self.disks[i].write(x[i])

    # Read all data on disks, ignoring parity bits and padding. Does not account for missing disks.
    def read_all_data(self):
        ret_str = ''
        for i in range(len(self)):
            for j in range(len(self.disks)):
                parity_disk = self.calculate_parity_disk(i)
                if j != parity_disk:
                    ret_str += chr(int(self.disks[j].read(i), 2))   # Convert bin string to integer, then to character
            for k in range(len(self.files)):
                if i == self.files[k].start_addr - 1:
                    ret_str = ret_str[:len(ret_str) - self.files[k-1].padding]

        ret_str = ret_str[:len(ret_str) - self.files[-1].padding]
        return ret_str

    # Read all data on disks, ignoring parity bits and padding. Does not account for missing disks.
    def read_all_files(self):
        ret_bits = []
        ret_files = []
        for i in range(len(self)):
            for j in range(self.num_disks):
                parity_disk = self.calculate_parity_disk(i)
                if j != parity_disk:
                    ret_bits.append(self.disks[j].read(i))
            for k in range(len(self.files)):
                if i == self.files[k].start_addr - 1:
                    ret_bits = ret_bits[:len(ret_bits) - self.files[k - 1].padding]
                    ret_files.append(RAIDFile.from_bits(k - 1, ret_bits))
                    ret_bits = []

        ret_bits = ret_bits[:len(ret_bits) - self.files[-1].padding]
        ret_files.append(RAIDFile.from_bits(self.files[-1].id, ret_bits))
        return ret_files

    # Simulate a disk failing by removing it from the list
    def disk_fails(self, disk_num):
        print("Disk " + repr(disk_num) + " failed")
        del self.disks[disk_num]

    # Reconstructs a failed disk.
    def reconstruct_disk(self, disk_num):
        print("Reconstructing Disk")
        if (self.num_disks - len(self.disks)) > 1:
            raise DiskReconstructException("Cannot reconstruct disk: too many disks missing")

        new_disk = Disk(disk_num, self.disk_cap)
        for i in range(len(self.disks[0])):
            block = []
            for j in range(len(self.disks)):
                block.append(self.disks[j].read(i))
            self.validate_parity(block + [format(self.calculate_parity(block), bin_format)])

            new_disk.write(format(self.calculate_parity(block), bin_format))
        self.disks.insert(disk_num, new_disk)
        self.validate_disks()

    # Validates the correctness of the parity for each stripe. If an original disk array is passed in, the Disk objects
    # in it are compared to the ones currently in the disk array to see if they contain the same data.
    def validate_disks(self, orig_disks=None):
        for i in range(len(self)):
            self.validate_parity(self.get_stripe(i))
        if orig_disks is not None:
            for i in range(len(orig_disks)):
                if orig_disks[i] != self.disks[i]:
                    raise DiskReconstructException("Disk reconstruction failed: Disk " + repr(i) + " corrupted")

    def calculate_parity_disk(self, index):
        return self.num_disks - ((index % self.num_disks) + 1)

    def print_data(self):
        for x in self.disks:
            print("|   " + repr(x.disk_id) + "    ", end="")
        print("|")
        for i in range(len(self.disks)):
            print("---------", end="")
        print("-")
        for i in range(len(self.disks[0])):
            parity_disk = self.calculate_parity_disk(i)
            for j in range(len(self.disks)):
                if i < len(self.disks[j]):
                    if self.disks[j].disk_id == parity_disk:
                        print("|" + Back.RED + Fore.BLACK + self.disks[j].read(i)[2:], end="")
                        print(Style.RESET_ALL, end="")
                    else:
                        print("|" + Back.YELLOW + Fore.BLACK + self.disks[j].read(i)[2:], end="")
                        print(Style.RESET_ALL, end="")
            print("|", end="")
            for f in self.files:
                if i == f.start_addr:
                    print("<- File " + repr(f.id), end="")
            print()
        print()

    # Calculate parity bit for block. We need to convert the bin strings to integers in order to use bit
    # manipulation to calculate the XOR
    @staticmethod
    def calculate_parity(block):
        calculated_parity = None
        for x in block:
            calculated_parity = calculated_parity ^ int(x, 2) if calculated_parity is not None else int(x, 2)
        return calculated_parity

    # Validates the parity of a block by removing each item in sequence, calculating the parity of the remaining items,
    # and comparing the result to the removed item.
    @staticmethod
    def validate_parity(block):
        for i in range(len(block)):
            parity = block.pop(i)
            calculated_parity = RAID5Controller.calculate_parity(block)
            if calculated_parity != int(parity,2):
                raise ParityCalculationException(block, calculated_parity, int(parity, 2))
            block.insert(i, parity)
