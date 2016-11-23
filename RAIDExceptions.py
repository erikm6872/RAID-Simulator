# CSCI 460 Final Project
# RAID-5 Simulator
#   RAIDExceptions.py
# Erik McLaughlin, Tyler Wright & Dave Robins
# 11/14/2016


class ParityCalculationException(Exception):
    def __init__(self, block=None, expected=None, actual=None):
        self.block = block
        self.expected = expected
        self.actual = actual

        if block is None or expected is None or actual is None:
            msg = "Incorrect parity bit calculation"
        else:
            msg = "Incorrect parity bit calculation\nBlock: "
            for x in block:
                msg += x + " "
            msg += "\nExpected: " + repr(expected) + " (" + format(expected, '#010b') + ")\n"
            msg += "Actual:   " + repr(actual) + " (" + format(actual, '#010b') + ")\n"
        super(ParityCalculationException, self).__init__(msg)


class DiskException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super(DiskException, self).__init__(msg)


class DiskReconstructException(DiskException):
    def __init__(self, msg):
        self.msg = msg
        super(DiskReconstructException, self).__init__(msg)


class DataMismatchException(DiskException):
    def __init__(self, msg):
        self.msg = msg
        super(DataMismatchException, self).__init__(msg)


