# CSCI 460 Final Project
# RAID-5 Simulator
#   Disk.py
# Erik McLaughlin & Tyler Wright
# 11/14/2016


class Disk:
    def __init__(self, disk_id):
        self.disk_id = disk_id
        self.data = []

    def __repr__(self):
        return repr(self.disk_id) + ":" + repr(self.data)

    def write(self, data):
        self.data.append(data)
