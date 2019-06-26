from __future__ import print_function
import sys
import os
from subprocess import Popen
import argparse
import time
from func import timer

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--python_exe',
                  dest="python_exe",
                  action="store")
parser.add_argument('--BetaBeatsrc_dir',
                  dest="BetaBeatsrc_dir",
                  action="store")
parser.add_argument('--model_dir',
                  dest="model_dir",
                  action="store")
parser.add_argument('--sdds_dir',
                  dest="sdds_dir",
                  action="store")
parser.add_argument('--phase_output_dir', '-pod',
                  dest="pod",
                  action="store")
parser.add_argument('--harmonic_output_dir', '-hod',
                  dest="hod",
                  action="store")
parser.add_argument('--mode',
                    choices=['harmonic', 'both'])
args = parser.parse_args()

# Check for output directories for Beta-Beat.src scripts
# If not present, create
if not os.path.exists(args.hod):
    os.system("mkdir " + args.hod)
if not os.path.exists(args.pod):
    os.system("mkdir " + args.pod)

if len(os.listdir(args.hod)) != 0:
    os.system("rm " + args.hod + "/*")
if len(os.listdir(args.pod)) != 0:
    os.system("rm -r " + args.pod + "/*")

# Run Beta-Beat.src srcripts in succession:
sdds_files = os.listdir(args.sdds_dir)
for i, run in enumerate(sdds_files):
    start = time.time()
    print(" ********************************************\n",
          "run_BetaBeatsrc.py:\n",
          '"Working on file ' + str(i) + '/' + str(len(sdds_files)) + ': ' + str(run) + '"\n',
          "********************************************")

    # hole_in_one.py
    p = Popen([args.python_exe,
               args.BetaBeatsrc_dir + 'hole_in_one.py',
               '--file', args.sdds_dir + run,
               '--outputdir', args.hod,
               '--model', args.model_dir + '/twiss.dat',
               '--startturn', '2',
               '--endturn', '2000',
               'harpy',
               '--harpy_mode', 'bpm',
               '--tunex=0.537',
               '--tuney=0.585',
               '--nattunex=0.537',
               '--nattuney=0.585',
               '--tolerance=0.025',
               '--tune_clean_limit=10e-5']) # changed from 1e-5 to 10e-5 so that fewer BPMs are cleaned
    p.wait()

    if args.mode == 'harmonic':
        break
    elif args.mode == 'both':
        # measure_optics.py
        p = Popen([args.python_exe,
                   args.BetaBeatsrc_dir + 'measure_optics.py',
                   '--model', args.model_dir,
                   '--accel', 'skekb',
                   '--files', args.hod + run,
                   '--output', args.pod + run + '/'])
        p.wait()

    finish = time.time() - start
    timer(i, len(sdds_files), finish)

sys.exit()
