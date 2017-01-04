# Imports

# Erik McLaughlin
# 12/1/2016
from RAID5Controller import *


'''
RAID-1: Data is mirrored on all disks. No parity calculations or striping.

'''


class RAID1Controller(RAIDController):
    __metaclass__ = RAIDController

    def write_bits(self, data):
        blocks = split_data(data, len(self.disks))

        for x in blocks:
            # Write block to disks
            for i in range(len(x)):
                for j in range(len(self.disks)):
                    self.disks[j].write(x[i])

        # Read all data on disks
    def read_all_data(self):
        ret_str = ''
        for i in range(len(self)):
            ret_str += chr(int(self.disks[0].read(i), 2))  # Convert bin string to integer, then to character
            for k in range(len(self.files)):
                if i == self.files[k].start_addr - 1:
                    ret_str = ret_str[:len(ret_str) - self.files[k - 1].padding]

        ret_str = ret_str[:len(ret_str) - self.files[-1].padding]
        return ret_str

    # Read all data on disks
    def read_all_files(self):
        ret_bits = []
        ret_files = []
        for i in range(len(self)):
            ret_bits.append(self.disks[0].read(i))
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
        if (self.num_disks - len(self.disks)) < 1:
            raise DiskReconstructException("Cannot reconstruct disk: no disks remaining")

        new_disk = Disk(self.disks[0])
        self.disks.insert(disk_num, new_disk)

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

    def validate_disks(self, orig_disks):
        pass
