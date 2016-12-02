#!/bin/bash
python3.5 main.py -h    # Show help dialog with argument options
echo

echo 5 disks, fail disk 2 and reconstruct, pausing between each step
read -n1 -r -p '$ python main.py -p'
python3.5 main.py -p
echo

echo 7 disks, fail disk 2 and reconstruct 
read -n1 -r -p '$ python main.py -n 7'
python3.5 main.py -n 7
echo

echo 5 disks, fail disk 0 and reconstruct 
read -n1 -r -p '$ python main.py -f 0'
python3.5 main.py -f 2
echo

echo 5 disks, fail each disk in sequence and reconstruct
read -n1 -r -p '$ python main.py --all'
python3.5 main.py --all
echo

echo 5 disks, different data strings
read -n1 -r -p '$ python main.py -d "The quick brown fox jumps " "over the lazy dog"'
python3.5 main.py -d "The quick brown fox jumps " "over the lazy dog"