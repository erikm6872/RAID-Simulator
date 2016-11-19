# CSCI 460 Final Project
# RAID-5 Simulator
#   RAIDController.py
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016
from Disk import Disk
from RAIDExceptions import *
from RAIDFile import *

def split_data(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]


class RAIDController:

    disks = []
    files = []

    def __init__(self, num_disks):
        self.num_disks = num_disks
        for i in range(num_disks):
            self.disks.append(Disk(i))

    def __len__(self):
        return len(self.disks[0])

    # Writes a string of bits to the RAID disks
    def __write_bits(self, data):
        blocks = split_data(data, len(self.disks)-1)

        for x in blocks:
            # Calculate parity bit for block x. We need to convert the bin strings to integers in order to use bit
            # manipulation to calculate the XOR

            parity_bit = self.calculate_parity(x)
            self.validate_parity(x + [format(parity_bit, '#010b')])

            parity_disk = self.calculate_parity_disk(len(self))

            # Insert the parity bit into the block at the position of the current parity disk
            x.insert(parity_disk, format(parity_bit, '#010b'))

            # Write block to disks
            for i in range(len(x)):
                self.disks[i].write(x[i])

    # Writes a RAIDFile object to disks
    def write_file(self, file):
        if len(self.files) == 0:
            file.start_addr = 0
        else:
            file.start_addr = len(self)

        self.files.append(file)
        blocks = list(split_data(file.data_B, len(self.disks) - 1))
        file.padding = (len(self.disks) - 1) - len(blocks[-1])
        self.__write_bits(file.data_B + [format(0, '#010b')] * file.padding)

    # Read all data on disks, ignoring parity bits and padding. Does not account for missing disks.
    def read_all(self):
        ret_str = ''
        ret_bits = []
        ret_files = []
        for i in range(len(self)):
            for j in range(self.num_disks):
                parity_disk = self.calculate_parity_disk(i)
                if j != parity_disk:
                    ret_str += chr(int(self.disks[j].read(i), 2))   # Convert bin string to integer, then to character
                    ret_bits.append(self.disks[j].read(i))
            for k in range(len(self.files)):
                if i == self.files[k].start_addr - 1:
                    ret_str = ret_str[:len(ret_str) - self.files[k-1].padding]
                    ret_bits = ret_bits[:len(ret_str) - self.files[k-1].padding]
                    ret_files.append(RAIDFile.from_bits(k-1, ret_bits))
                    ret_bits = []

        ret_str = ret_str[:len(ret_str) - self.files[-1].padding]

        ret_bits = ret_bits[:len(ret_str) - self.files[-1].padding]
        ret_files.append(RAIDFile.from_bits(self.files[-1].id, ret_bits))
        return ret_str

    # Simulate a disk failing by removing it from the list
    def disk_fails(self, disk_num):
        print("Disk " + repr(disk_num) + " failed")
        del self.disks[disk_num]

    # Reconstructs a failed disk.
    def reconstruct_disk(self, disk_num):
        if (self.num_disks - len(self.disks)) > 1:
            raise DiskReconstructException("Cannot reconstruct disk: too many disks missing")

        new_disk = Disk(disk_num)
        for i in range(len(self.disks[0])):
            block = []
            for j in range(len(self.disks)):
                block.append(self.disks[j].read(i))
            self.validate_parity(block + [format(self.calculate_parity(block), '#010b')])

            new_disk.write(format(self.calculate_parity(block), '#010b'))
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

    # Returns a stripe of data from the disk array.
    def get_stripe(self, index):
        block = []
        for i in range(len(self.disks)):
            try:
                block.append(self.disks[i].read(index))
            except IndexError:
                pass
        return block

    def calculate_parity_disk(self, index):
        return self.num_disks - ((index % self.num_disks) + 1)

    # Prints the data on each disk in a table. Parity bits are marked with '*'
    def print_data(self):
        for x in self.disks:
            print("|    " + repr(x.disk_id) + "     ", end="")
        print("|")
        for i in range(len(self.disks)):
            print("-----------", end="")
        print("-")
        for i in range(len(self.disks[0])):
            parity_disk = self.calculate_parity_disk(i)
            for j in range(len(self.disks)):
                if i < len(self.disks[j]):
                    print("| " + self.disks[j].read(i)[2:], end="")
                    if j == parity_disk:
                        print("*", end="")
                    else:
                        print(" ", end="")
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
            calculated_parity = RAIDController.calculate_parity(block)
            if calculated_parity != int(parity,2):
                raise ParityCalculationException(block, calculated_parity, int(parity, 2))
            block.insert(i, parity)
