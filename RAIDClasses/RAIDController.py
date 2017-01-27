# CSCI 460 Final Project
# RAID-5 Simulator
#   RAIDController.py
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016
from Disk import Disk
from RAIDFile import *
from abc import abstractmethod, ABCMeta
from RAIDExceptions import *


def split_data(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]


class RAIDController(metaclass=ABCMeta):
    files = []
    disks = []

    def __init__(self, num_disks, disk_cap=0):
        self.num_disks = num_disks
        self.disk_cap = disk_cap
        for i in range(num_disks):
            self.disks.append(Disk(i, disk_cap))

    def __len__(self):
        return len(self.disks[0])

    def get_stripe(self, index):
        # Returns a stripe of data from the disk array.
        block = []
        for i in range(len(self.disks)):
            try:
                block.append(self.disks[i].read(index))
            except IndexError:
                pass
        return block

    # Overridden in RAID0Controller
    def write_file(self, file):
        if len(self.files) == 0:
            file.start_addr = 0
        else:
            file.start_addr = len(self)

        self.files.append(file)
        blocks = list(split_data(file.data_B, len(self.disks) - 1))
        file.padding = (len(self.disks) - 1) - len(blocks[-1])
        self.write_bits(file.data_B + [format(0, bin_format)] * file.padding)


    # Validates the correctness of the parity for each stripe. If an original disk array is passed in, the Disk objects
    # in it are compared to the ones currently in the disk array to see if they contain the same data.
    def validate_disks(self, orig_disks=None):
        for i in range(len(self)):
            self.validate_parity(self.get_stripe(i))
        if orig_disks is not None:
            for i in range(len(orig_disks)):
                if orig_disks[i] != self.disks[i]:
                    raise DiskReconstructException("Disk reconstruction failed: Disk " + repr(i) + " corrupted")

    @abstractmethod
    def write_bits(self, data):
        pass

    @abstractmethod
    def read_all_data(self):
        pass

    @abstractmethod
    def read_all_files(self):
        pass

    @abstractmethod
    def disk_fails(self, disk_num):
        pass

    @abstractmethod
    def reconstruct_disk(self, disk_num):
        pass

    @abstractmethod
    def print_data(self):
        pass
