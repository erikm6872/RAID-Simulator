# RAID Simulator
#### [Erik McLaughlin](https://erikcmclaughlin.com), Tyler Wright & Dave Robins

## Description
RAID Simulator is an open source tool written in Python used to demonstrate the differences in RAID levels. 
This is an ongoing project, currently only RAID levels 0, 1, 4 and 5 are implemented.

## Prerequisites
* Python 3.5
* [Colorama 0.3.7](https://pypi.python.org/pypi/colorama)

## Run
* `$ python main.py`

## Arguments
```
usage: main.py [-h] [-n DISKS] [-l {0,1,2,3,4,5,6}] [-c CAP] [-f DISK] [-a]
               [-d [DATA [DATA ...]]] [-p]

RAID-5 Simulator

optional arguments:
  -h, --help            show this help message and exit
  -n DISKS, --numdisks DISKS
                        Number of disks in the RAID array. Default=5
  -l {0,1,2,3,4,5,6}, --level {0,1,2,3,4,5,6}
                        RAID level to simulate. Default=5
  -c CAP, --capacity CAP
                        Storage capacity of each disk in bytes. Default=0
                        (unlimited)
  -f DISK, --fail DISK  Disk number to fail. Default=2
  -a, --all             Fail each disk in sequence.
  -d [DATA [DATA ...]], --data [DATA [DATA ...]]
                        Data strings to write to the disks array. Default is a
                        series of Lorem Ipsum strings.
  -p, --pause           Pause script between major actions. Used for demo
                        purposes.
```
