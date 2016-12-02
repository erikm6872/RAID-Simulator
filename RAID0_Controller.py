# Imports

# Erik McLaughlin
# 12/1/2016
from RAIDController import *


class RAID0_Controller(RAIDController):
    def __init__(self, num_disks, disk_cap=0):
        super(RAID0_Controller, self).__init__(num_disks, disk_cap)

    def __write_bits(self, data):
        blocks = split_data(data, len(self.disks))

        for x in blocks:
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
        blocks = list(split_data(file.data_B, len(self.disks)))
        file.padding = (len(self.disks)) - len(blocks[-1])
        self.__write_bits(file.data_B + [format(0, bin_format)] * file.padding)

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
        raise RuntimeWarning("RAID-0 does not support disk reconstruction")

    # Reconstructs a failed disk.
    def reconstruct_disk(self, disk_num):
        raise RuntimeError("Raid-0 does not support disk reconstruction")
