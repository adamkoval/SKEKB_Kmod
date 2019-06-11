from __future__ import print_function
import sys
import os
from subprocess import Popen
import argparse

# Argument parser.
parser = argparse.ArgumentParser()
parser.add_option('--python_exe',
                  dest="python_exe",
                  action="store")
parser.add_option('--BetaBeatsrc_dir',
                  dest="BetaBeatsrc_dir",
                  action="store")
parser.add_option('--model_dir',
                  dest="model_dir",
                  action="store")
parser.add_option('--sdds_dir',
                  dest="sdds_dir",
                  action="store")
parser.add_option('--phase_output_dir', '-pod',
                  dest="pod",
                  action="store")
parser.add_option('--harmonic_output_dir', '-hod',
                  dest="hod",
                  action="store")
args = parser.parse_args()

# Check for output directories for Beta-Beat.src scripts.
# If not present, create.
if not os.path.exists(args.hod):
    os.system("mkdir " + args.hod)
if not os.path.exists(args.pod):
    os.system("mkdir " + args.pod)

if len(os.listdir(args.hod)) != 0:
    os.system("rm " + args.hod + "/*")
if len(os.listdir(args.pod)) != 0:
    os.system("rm -r " + args.pod + "/*")

# Run Beta-Beat.src srcripts in succession:
for run in os.listdir(args.sdds_dir):
    print("working on file", run)

    # hole_in_one.py
    p = Popen([args.python_exe,
               args.BetaBeatsrc_dir + 'hole_in_one.py',
               '--file', args.sdds_dir + run,
               '--outputdir', args.hod,
               '--model', args.model_dir + '/twiss.dat',
               '--startturn', '2',
               '--endturn', '4000',
               'harpy',
               '--harpy_mode', 'bpm',
               '--tunex=0.546',
               '--tuney=0.612',
               '--nattunex=0.546',
               '--nattuney=0.612',
               '--tolerance=0.01',
               '--tune_clean_limit=10e-5']) # changed from 1e-5 to 10e-5 so that fewer BPMs are cleaned
    p.wait()

    # measure_optics.py
    p = Popen([args.python_exe,
               args.BetaBeatsrc_dir + 'measure_optics.py',
               '--model', args.model_dir,
               '--accel', 'skekb',
               '--files', args.hod + run,
               '--output', args.pod + run + '/'])
    p.wait()

sys.exit()
