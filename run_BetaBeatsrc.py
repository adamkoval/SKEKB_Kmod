from __future__ import print_function
import sys
import os
from subprocess import Popen
import optparse

parser = optparse.OptionParser()
parser.add_option('--python_exe', action="store", dest="python_exe")
parser.add_option('--BetaBeatsrc_dir', action="store", dest="BetaBeatsrc_dir")
parser.add_option('--model_dir', action="store", dest="model_dir")
parser.add_option('--sdds_dir', action="store", dest="sdds_dir")
parser.add_option('--phase_output_dir', action="store", dest="phase_output_dir")
parser.add_option('--harmonic_output_dir', action="store", dest="harmonic_output_dir")
options, args = parser.parse_args()

if not os.path.exists(options.harmonic_output_dir):
    os.system("mkdir " + options.harmonic_output_dir)
if not os.path.exists(options.phase_output_dir):
    os.system("mkdir " + options.phase_output_dir)

if len(os.listdir(options.harmonic_output_dir)) != 0:
    os.system("rm " + options.harmonic_output_dir + "/*")
if len(os.listdir(options.phase_output_dir)) != 0:
    os.system("rm -r " + options.phase_output_dir + "/*")

for run in os.listdir(options.sdds_dir):
    p = Popen([options.python_exe,
               options.BetaBeatsrc_dir + 'hole_in_one.py',
               '--file', options.sdds_dir + run,
               '--outputdir', options.harmonic_output_dir,
               '--model', options.model_dir + '/twiss.dat',
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

    output = options.phase_output_dir + run + '/'
    p = Popen([options.python_exe,
               options.BetaBeatsrc_dir + 'measure_optics.py',
               '--model', options.model_dir,
               '--accel', 'skekb',
               '--files', options.harmonic_output_dir + run,
               '--output', options.phase_output_dir + run + '/'])
    p.wait()
    print("working on file", run)

sys.exit()
