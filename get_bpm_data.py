#===========================================================
#   Edited by Adam Koval (24/5/19)
#===========================================================
from __future__ import print_function
import os
import sys
from subprocess import Popen
from func import read_pathnames, look_for_dict, generic_dict

pathnames = read_pathnames()

ringID = pathnames["ringID"]
init_path = pathnames["init_path"]
lattice_file = pathnames["lattice_file"]
ftwissbpm = pathnames["ftwissbpm"]
ftwissall = pathnames["ftwissall"]
fkmodu = pathnames["fkmodu"]

# Paths to executables
gsad = pathnames["gsad"]
python_exe = pathnames["python_exe"]
BetaBeatsrc_path = pathnames["BetaBeatsrc_path"]

# Input directories
data_input_dir = pathnames["data_input_dir"]
model_dir = pathnames["model_dir"]

# Output directories
temp_dir = pathnames["temp_dir"]
harmonic_output_dir = pathnames["harmonic_output_dir"]
phase_output_dir = pathnames["phase_output_dir"]

# Checking for a dictionary
while True:
    if look_for_dict(init_path) == True:
        break
    else:
        user_input = raw_input('There is no dictionary file present. Would you like to create a new one (input -> create) or would you like to provide one (input -> provide)?\n')
        if user_input == 'create':
            generic_dict(data_input_dir, ringID, init_path)
            continue
        elif user_input == 'provide':
            continue

# Checking if temp/ dir exists or is empty
if os.path.exists(temp_dir):
    os.system("rm -r " + temp_dir + "*")
else:
    os.system("mkdir " + temp_dir)

# Conversion without asynch knowledge
file = open("prerun.sad", "w")
file.write(' READ "' + init_path + lattice_file + '";\n'
           ' FFS;\n'
           '\n'
           ' ring = "' + ringID + '";\n'
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
           ' runs = Get["' + init_path + 'file_dict.txt"];\n'
           ' Do[\n'
           '   fnr1 = "./"//runs[i, 1];\n'
           '   fbpm = "None";\n' # This line tells FormatBPMRead[] to convert without synch fix
           '   fwt1 = "' + temp_dir + '"//runs[i, 2];\n'
           '   FormatBPMRead[fnr1, fwt1, fbpm];\n'
           '   Print["Converting "//runs[i, 1]//" -> "//runs[i, 2]];\n'
           #'   ,{i, 1, Length[runs]}];\n'
           '   ,{i, 1, 2}];\n' # Only does two runs for debugging purposes.
           '\n'
           ' abort;\n')
file.close()

os.system(gsad + " prerun.sad")
print(" *******************************\n",
      "prerun.sad finished, running analysis script.\n",
      "*******************************")

# Beta-Beat.src analysis
p = Popen([python_exe,
           'run.py',
           '--python_exe', python_exe,
           '--BetaBeatsrc_dir', BetaBeatsrc_path,
           '--model_dir', model_dir,
           '--sdds_dir', temp_dir,
           '--harmonic_output_dir', harmonic_output_dir,
           '--phase_output_dir', phase_output_dir])
p.wait()
print(" *******************************\n",
      "Beta-Beat.src analysis finished, checking asynchronous BPMs.\n",
      "*******************************")

# Asynch analysis
# NOTE: This analysis is being run for the x-axis as this one has been found to
#       have cleaner results.
p = Popen([python_exe,
           'async.py',
           '--phase_output_dir', phase_output_dir,
           '--async_output_dir', 'outofphasex/',
           '--axis', 'x'])
p.wait()
print(" *******************************\n",
      "Asynchronous BPMs found, converting raw -> sdds with synch fix.\n",
      "*******************************")

# Conversion with asynch knowledge + KModu simulation
file = open("run.sad", "w")
file.write(' READ "' + init_path + lattice_file + '";\n'
           ' FFS;\n'
           '\n'
           ' ring = "' + ringID + '";\n'
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
           #' BPMpath = "./KEK_datafiles/";\n'           
           ' fn1 = "' + ftwissbpm + '";\n'
           ' fn2 = "' + ftwissall + '";\n'
           ' SaveTwiss[fn1, fn2];\n\n'
           ' runs = Get["' + init_path + 'file_dict.txt"];\n'
           #' end;\n\n' # --> comment it
           ' Do[\n'
           '   fnr1 = "./"//runs[i, 1];\n'
           '   fbpm = "' + init_path + 'BPMlist.txt";\n'
           '   fwt1 = "' + temp_dir + '"//runs[i, 2];\n'
           '   FormatBPMRead[fnr1, fwt1, fbpm];\n'
           '   Print["Converting "//runs[i, 1]//" -> "//runs[i, 2]];\n'
           #'   ,{i, 1, Length[runs]}];\n'
           '   ,{i, 1, 2}];\n' # Only does two runs for debugging purposes.
           '\n'
           # Kmodu simulation
           '! Couple quadrupole slices in the IR\n'
           ' If[ring=="HER",\n'
           '    FFS["CoupLER2HERPartition[];"],\n'
           '    FFS["CoupHER2LERPartition[];"]\n'
           '    ];\n'
           '\n'
           '! Kmodu assessment in SAD\n'
           ' GetQCInfo[ring];\n'
           ' GetTMATRIX[ring];\n'
           ' QCK1Twiss0 = GetQCValueTwiss[]; ! initial setting\n'
           '\n'
           ' Kkmodu = {1-0.0005, 1, 1+0.0005};\n' #
           ' {NX1L, NY1L} = GetTuneKmodu[QC1L, Kkmodu];\n'
           ' {NX2L, NY2L} = GetTuneKmodu[QC2L, Kkmodu];\n'
           ' {NX1R, NY1R} = GetTuneKmodu[QC1R, Kkmodu];\n'
           ' {NX2R, NY2R} = GetTuneKmodu[QC2R, Kkmodu];\n'
           '\n'
           ' fn3 = "' + fkmodu + '";\n'
           ' WriteIRInformation[fn3, ring];\n'
           ' AppendTuneModu[fn3, Kkmodu];\n'

           #' end;\n'
           ' abort;\n')
file.close()

os.system(gsad + " run.sad");
print(" *******************************\n",
      "run.sad finished, running analysis script.\n",
      "*******************************")

# Beta-Beat.src analysis
p = Popen([python_exe,
           'run.py',
           '--python_exe', python_exe,
           '--BetaBeatsrc_dir', BetaBeatsrc_path,
           '--model_dir', model_dir,
           '--sdds_dir', temp_dir,
           '--harmonic_output_dir', harmonic_output_dir,
           '--phase_output_dir', phase_output_dir])
p.wait()
print(" *******************************\n",
      "Beta-Beat.src analysis finished, data is ready.\n"
      "*******************************")

sys.exit()
