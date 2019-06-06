#===========================================================
#   
#  Edited by Adam Koval (24/5/19)
#===========================================================
import os
import sys
from subprocess import Popen
from func import read_pathnames

pathnames = read_pathnames()

ringID = pathnames["ringID"]
initpath = pathnames["init_path"]
latticefile = pathnames["lattice_file"]
ftwissbpm = pathnames["ftwissbpm"]
ftwissall = pathnames["ftwissall"]
fkmodu = pathnames["fkmodu"]

# Paths to executables
gsad = pathnames["gsad"]
python_exe = pathnames["python_exe"]
BetaBeatsrcPath = pathnames["BetaBeatsrc_path"]

# Output directories
respath = pathnames["temp_path"]
harmonic_output_dir = pathnames["harmonic_output_dir"]
phase_output_dir = pathnames["phase_output_dir"]

# Conversion without asynch knowledge
file = open("prerun.sad", "w")
file.write(' READ "'+initpath+latticefile+'";\n'
           ' FFS;\n'
           '\n'
           ' ring = "'+ringID+'";\n'
           ' If[ring=="HER",\n'
           '   FFS["USE ASCE"],\n'
           '   If[ring=="LER",\n'
           '     FFS["USE ASC"],\n'
           '     Print["\t >> Enter correct ringID (HER or LER)"];\n'
           '     FFS["end"]\n'
           '     ]\n'
           '   ]\n'
           ' CELL; CALC;\n'
           ' emit;\n\n'
           ' Get["func.n"];\n\n'
           ' runs = Get["'+initpath+'file_dict.txt"];\n'
           ' Do[\n'
           '   fnr1 = "./"//runs[i, 1];\n'
           '   fbpm = "None";\n' # This line tells FormatBPMRead[] to convert without synch fix
           '   fwt1 = "' + respath + '"//runs[i, 2];\n'
           '   FormatBPMRead[fnr1, fwt1, fbpm];\n'
           '   Print["Converting "//runs[i, 1]//" -> "//runs[i, 2]];\n'
           #'   ,{i, 1, Length[runs]}];\n'
           '   ,{i, 1, 2}];\n'
           '\n'
           ' abort;\n')
file.close()

os.system(gsad + " prerun.sad")
print("prerun.sad finished, running analysis script.")

sys.exit()

# Beta-Beat.src analysis
p = Popen([python_exe,
           'run.py',
           '--python_exe', python_exe,
           '--BetaBeatsrc_dir', BetaBeatsrcPath,
           '--model_dir', 'model/',
           '--sdds_dir', 'temp/',
           '--harmonic_output_dir', harmonic_output_dir,
           '--phase_output_dir', phase_output_dir])
p.wait()
print("Beta-Beat.src analysis finished, checking asynchronous BPMs.")

sys.exit()
