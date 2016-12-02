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