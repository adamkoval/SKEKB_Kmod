"""
Created on Tue Jun 11
Author: Adam Koval
"""
from __future__ import print_function
import argparse

# Argument parser.
parser = argparse.ArgumentParser()
parser.add_argument('--axis', '-ax',
                    dest='axis',
                    action='store')
parser.add_argument('--async_output_dir',
                    dest='aod',
                    action='store')
parser.add_argument('--phase_output_dir',
                    dest='pod',
                    action='store')
args = parser.parse_args()

# All else

