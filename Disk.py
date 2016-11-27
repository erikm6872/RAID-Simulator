# CSCI 460 Final Project
# RAID-5 Simulator
#   Disk.py
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016
from RAIDExceptions import *


class Disk:
    def __init__(self, disk_id, capacity=0):
        self.disk_id = disk_id
        self.capacity = capacity
        self.data = []

    def __repr__(self):
        return repr(self.disk_id) + ":" + repr(self.data)

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def write(self, data):
        if (self.capacity > 0) and (len(self.data) + len(data) > self.capacity):
            raise DiskFullException(self.disk_id)
        self.data.append(data)

    def read(self, index):
        if index >= len(self.data):
            raise DiskReadException("Cannot read index '" + repr(index) + "' on disk '" + repr(self.disk_id) +
                                    "': Index out of bounds")
        return self.data[index]
