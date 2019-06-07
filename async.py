"""
Created on Thu Oct 18 14:56:32 2018
Edited on Fri May 24
Author: Adam Koval
"""
from __future__ import print_function
import sys
import os
import numpy as np
import optparse
from func import phase, phasetot

parser = optparse.OptionParser()
parser.add_option('--phase_output_dir', action="store", dest="phase_output_dir")
parser.add_option('--async_output_dir', action="store", dest="async_output_dir")
parser.add_option('--axis', action="store", dest="axis")
options, args = parser.parse_args()

if not os.path.exists(options.phase_output_dir):
    print("Directory", options.phase_output_dir, "not found.")
    sys.exit()
if not os.path.exists(options.async_output_dir):
    os.system("mkdir " + options.async_output_dir)

for run in os.listdir(options.phase_output_dir):
    datapath = options.phase_output_dir + run + '/'
    try:
        S, names, deltaph, phx, phxmdl, Qx, Qy = phase(datapath, options.axis)
    except IOError:
        continue
    deltaphtot = phasetot(datapath, options.axis)

    level = []
    for i in range(len(deltaphtot)):
        if deltaphtot[i] / Qx >= .5:
            level.append('-1')
        elif deltaphtot[i] / Qx <= -.5:
            level.append('+1')
        elif deltaphtot[i] / Qx > -.5 and deltaphtot[i] / Qx < .5:
            level.append('0')
    file = open(options.async_output_dir + run + '.txt', 'w')
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
