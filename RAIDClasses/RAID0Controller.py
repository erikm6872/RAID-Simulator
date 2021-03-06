# Imports

# Erik McLaughlin
# 12/1/2016
import warnings

from RAIDClasses.RAID5Controller import *

'''
RAID-0: Data is striped across all disks without parity calculations.

'''


class RAID0Controller(RAIDController):
    __metaclass__ = RAIDController

    def write_bits(self, data):
        blocks = split_data(data, len(self.disks))

        for x in blocks:
            # Write block to disks
            for i in range(len(x)):
                self.disks[i].write(x[i])

        # Read all data on disks, ignoring parity bits and padding. Does not account for missing disks.
    def read_all_data(self):
        ret_str = ''
        for i in range(len(self)):
            for j in range(len(self.disks)):
                ret_str += chr(int(self.disks[j].read(i), 2))  # Convert bin string to integer, then to character
            for k in range(len(self.files)):
                if i == self.files[k].start_addr - 1:
                    ret_str = ret_str[:len(ret_str) - self.files[k - 1].padding]

        ret_str = ret_str[:len(ret_str) - self.files[-1].padding]
        return ret_str

    # Read all data on disks, ignoring parity bits and padding. Does not account for missing disks.
    def read_all_files(self):
        ret_bits = []
        ret_files = []
        for i in range(len(self)):
            for j in range(self.num_disks):
                try:
                    ret_bits.append(self.disks[j].read(i))
                except IndexError:
                    pass
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
        del self.disks[disk_num]
        warnings.warn("Raid-0 does not support disk reconstruction.")
        # raise RuntimeWarning("RAID-0 does not support disk reconstruction")

    # Reconstructs a failed disk.
    def reconstruct_disk(self, disk_num):
        # raise RuntimeError("Raid-0 does not support disk reconstruction")
        warnings.warn("Raid-0 does not support disk reconstruction.")

    def print_data(self):
        for x in self.disks:
            print("|   " + repr(x.disk_id) + "    ", end="")
        print("|")
        for i in range(len(self.disks)):
            print("---------", end="")
        print("-")
        for i in range(len(self.disks[0])):
            for j in range(len(self.disks)):
                if i < len(self.disks[j]):
                    print("|" + self.disks[j].read(i)[2:], end="")
            print("|", end="")
            for f in self.files:
                if i == f.start_addr:
                    print("<- File " + repr(f.id), end="")
            print()
        print()

    # Needs to be overridden because the padding is different when parity is not used.
    def write_file(self, file):
        if len(self.files) == 0:
            file.start_addr = 0
        else:
            file.start_addr = len(self)

        self.files.append(file)
        blocks = list(split_data(file.data_B, len(self.disks)))
        file.padding = len(self.disks) - len(blocks[-1])
        self.write_bits(file.data_B + [format(0, bin_format)] * file.padding)
