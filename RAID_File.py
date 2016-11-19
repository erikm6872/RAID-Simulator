# CSCI 460 Final Project
# RAID-5 Simulator
#   RAID_File.py
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016


class RAIDFile:
    data_B = []
    start_addr = None
    padding = 0

    def __init__(self, data):
        self.data_S = data
        self.data_B = self.convert_string(data)

    def __len__(self):
        return len(self.data_B)

    @staticmethod
    def convert_string(d):
        bin_list = []
        for x in d:
            bin_list.append(format(ord(x), '#010b'))  # Change character -> integer -> binary string and append to list
        return bin_list
