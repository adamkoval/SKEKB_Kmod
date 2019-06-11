from __future__ import print_function
import sys
import os
from subprocess import Popen
import argparse

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
parser.add_option('--phase_output_dir',
                  dest="phase_output_dir",
                  action="store")
parser.add_option('--harmonic_output_dir',
                  dest="harmonic_output_dir",
                  action="store")
args = parser.parse_args()

if not os.path.exists(args.harmonic_output_dir):
    os.system("mkdir " + args.harmonic_output_dir)
if not os.path.exists(args.phase_output_dir):
    os.system("mkdir " + args.phase_output_dir)

if len(os.listdir(args.harmonic_output_dir)) != 0:
    os.system("rm " + args.harmonic_output_dir + "/*")
if len(os.listdir(args.phase_output_dir)) != 0:
    os.system("rm -r " + args.phase_output_dir + "/*")

for run in os.listdir(args.sdds_dir):
    p = Popen([args.python_exe,
               args.BetaBeatsrc_dir + 'hole_in_one.py',
               '--file', args.sdds_dir + run,
               '--outputdir', args.harmonic_output_dir,
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

    output = args.phase_output_dir + run + '/'
    p = Popen([args.python_exe,
               args.BetaBeatsrc_dir + 'measure_optics.py',
               '--model', args.model_dir,
               '--accel', 'skekb',
               '--files', args.harmonic_output_dir + run,
               '--output', args.phase_output_dir + run + '/'])
    p.wait()
    print("working on file", run)

sys.exit()
