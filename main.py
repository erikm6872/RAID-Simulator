# CSCI 460 Final Project
# RAID-5 Simulator
#
# Erik McLaughlin & Tyler Wright
# 11/14/2016
from RAIDController import *


# "Hello World" in binary
data = "011010000110010101101100011011000110111100100000011101110110111101110010011011000110010000001010"


def main():
    controller = RAIDController(5)
    controller.write_string(convert_string(data))
    controller.print_data()


def convert_string(d):
    bin_str = []
    for x in d:
        bin_str.append(int(x))
    return bin_str

main()
