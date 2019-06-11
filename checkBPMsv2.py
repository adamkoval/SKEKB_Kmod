"""
Created on Tue Jun 11
Author: Adam Koval
"""
from __future__ import print_function
import os
import argparse
from func import BPMs_from_sdds, get_all_outofsynch, get_dict

# Argument parser.
parser = argparse.ArgumentParser()
parser.add_argument('--axis', '-ax',
                    dest='axis',
                    action='store')
parser.add_argument('--async_output_dir', '-aod',
                    dest='async_output_dir',
                    action='store')
parser.add_argument('--main_output_dir', '-mod',
                    dest='main_output_dir',
                    action='store')
parser.add_argument('--sdds_dir',
                    dest='sdds_dir',
                    action='store')
args = parser.parse_args()

# All else
# Getting list of BPMs from any sdds file.
BPMlist = BPMs_from_sdds(os.listdir(args.sdds_dir)[0])

# Getting a dictionary of all files from outofsynch dir.
all_outofsynch = (args.async_output_dir, args.axis)


