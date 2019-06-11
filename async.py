"""
Created on Thu Oct 18 14:56:32 2018
Edited on Fri May 24
Author: Adam Koval
"""
from __future__ import print_function
import sys
import os
import numpy as np
import argparse
from func import phase, phasetot

# Argument parser.
parser = argparse.ArgumentParser()
parser.add_argument('--phase_output_dir',
                    dest="phase_output_dir",
                    action="store")
parser.add_argument('--async_output_dir',
                    dest="async_output_dir",
                    action="store")
parser.add_argument('--axis',
                    dest="axis",
                    action="store")
args = parser.parse_args()

# Check if phase output directory exists, if not, exit.
if not os.path.exists(args.phase_output_dir):
    print("Directory", args.phase_output_dir, "not found.")
    sys.exit()
# Check if output dir for the present script exists, if not, create one.
if not os.path.exists(args.async_output_dir):
    os.system("mkdir " + args.async_output_dir)

# Check for asynchronous BPMs in each measurement reun using phase output.
for run in os.listdir(args.phase_output_dir):
    datapath = args.phase_output_dir + run + '/'
    try:
        S, names, deltaph, phx, phxmdl, Qx, Qy = phase(datapath, args.axis)
    except IOError:
        continue
    deltaphtot = phasetot(datapath, args.axis)

    level = []
    for i in range(len(deltaphtot)):
        if deltaphtot[i] / Qx >= .5:
            level.append('-1')
        elif deltaphtot[i] / Qx <= -.5:
            level.append('+1')
        elif deltaphtot[i] / Qx > -.5 and deltaphtot[i] / Qx < .5:
            level.append('0')
    file = open(args.async_output_dir + run + '.txt', 'w')
    file.write('{\n')
    g = 0
    try:
        for i in range(len(names)):
            if g != 0:
                file.write(',\n')
            file.write('"' + names[i] + '"->' + level[i])
            g += 1
    except IndexError:
        print(run)
        print(len(level))
        print(len(deltaphtot))
    file.write('\n}')
    file.close()

sys.exit()
