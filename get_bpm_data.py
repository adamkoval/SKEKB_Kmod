#===========================================================
#   Originally written by R. Yang, edited by A. Koval
#===========================================================
from __future__ import print_function
import os
import sys
import argparse
from subprocess import Popen
from func import read_pathnames, look_for_dict, generic_dict

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--debug', '-db',
                    action='store_true')
parser.add_argument('--pathnames',
                    action='store',
                    dest='pathnames')
parser.add_argument('--bpmanalysis_off', '-bpma_off',
                    action='store_true')
parser.add_argument('--plotbpma',
                    action='store_true')
parser.add_argument('--BetaBeatsrc_mode',
                    choices=['harmonic', 'both'])
args = parser.parse_args()

# Checking for debug option
if args.debug == True:
    loopend = '2'
else:
    loopend = 'Length[runs]'

# Read in destinations
pathnames = read_pathnames(args.pathnames)

# General
ringID = pathnames["ringID"]
lattice_dir = pathnames["lattice_dir"]
if not pathnames["lattice_name"] == '~':
    lattice_name = pathnames["lattice_name"]
else:
    pass
file_dict = pathnames["file_dict"]

# Paths to executables
gsad = pathnames["gsad"]
python_exe = pathnames["python_exe"]
BetaBeatsrc_path = pathnames["BetaBeatsrc_path"]

# Input directories
input_data_dir = pathnames["input_data_dir"]
model_dir = pathnames["model_dir"]

# Output directories
main_output_dir = pathnames["main_output_dir"]
temp_dir = pathnames["temp_dir"]
harmonic_output_dir = main_output_dir + "harmonic_output/"
phase_output_dir = main_output_dir + "phase_output/"

# Output files
ftwissbpm = main_output_dir + pathnames["ftwissbpm"]
ftwissall = main_output_dir + pathnames["ftwissall"]
fkmodu = main_output_dir + pathnames["fkmodu"]


def sdds_conv():
    # If you are starting from clean dir, you must have a dictionary
    # Checking for a dictionary                                         
    while True:
        if look_for_dict(file_dict) == True:
            break
        else:
            user_input = raw_input('There is no dictionary file present for .data -> .sdds conversion. Would you like to create a new one (input -> create) or would you like to provide one (input -> provide)?\n')
            if user_input == 'create':
                generic_dict(input_data_dir, ringID, file_dict)
                continue
            elif user_input == 'provide':
                continue

    # Conversion without asynch knowledge
    file = open("prerun.sad", "w")
    file.write(' READ "' + lattice_dir + lattice_name + '";\n'
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
               ' runs = Get["' + file_dict + '"];\n'
               ' Do[\n'
               '   fnr1 = "./"//runs[i, 1];\n'
               '   fbpm = "None";\n' # This line tells FormatBPMRead[] to convert without synch fix
               '   fwt1 = "' + temp_dir + '"//runs[i, 2];\n'
               '   FormatBPMRead[fnr1, fwt1, fbpm];\n'
               '   Print["Converting "//runs[i, 1]//" -> "//runs[i, 2]];\n'
               '   ,{i, 1, ' + loopend + '}];\n'
               '\n'
               ' abort;\n')
    file.close()

    os.system(gsad + " prerun.sad")
    return print(" ********************************************\n",
                 "get_bpm_data.py:\n",
                 '"prerun.sad finished, running analysis script."\n',
                 "********************************************")

# Checking if temp/ dir exists
if os.path.exists(temp_dir):
    # Checking if it is empty
    if os.listdir(temp_dir):
        while True:
            user_input = raw_input('sdds (temp) directory contains files. Would you like to clean the directory and start anew (options: yes, no, show contents)?\n')
            if user_input == 'yes':
                os.system("rm -r " + temp_dir + "*")
                sdds_conv()
                break
            elif user_input == 'no':
                break
            elif user_input == 'show contents':
                os.system('ls ' + temp_dir)
                continue
            else:
                print('Please enter a valid string (see "options").')
                continue
    else:
        sdds_conv()
else:
    os.system("mkdir " + temp_dir)
    sdds_conv()


def betabeatanalysis():
    p = Popen([python_exe,
               'run_BetaBeatsrc.py',
               '--python_exe', python_exe,
               '--BetaBeatsrc_dir', BetaBeatsrc_path,
               '--model_dir', model_dir,
               '--sdds_dir', temp_dir,
               '--harmonic_output_dir', harmonic_output_dir,
               '--phase_output_dir', phase_output_dir,
               '--mode', args.BetaBeatsrc_mode])
    p.wait()
    return print(" ********************************************\n",
                 "get_bpm_data.py:\n",
                 '"Beta-Beat.src analysis finished, checking asynchronous BPMs."\n',
                 "********************************************")

# Beta-Beat.src analysis
if os.path.exists(main_output_dir):
    while True:
        user_input = raw_input('Would you like to clean the output directory and start anew (options: yes, no, show_contents)?\n')
        if user_input == 'yes':
            os.system("rm -r " + main_output_dir + "*")
            betabeatanalysis()
            break
        elif user_input == 'no':
            break
        elif user_input == 'show_contents':
            os.system('ls ' + main_output_dir)
            continue
        else:
            print('Please enter a valid string (see "options").')
            continue
else:
    os.system("mkdir " + main_output_dir)
    betabeatanalysis()

# Asynch analysis before
# NOTE: This analysis is being run for both axes, but the x-axis is used
#       in run.sad (generated below) as this one has been found to have 
#       cleaner results.
if args.bpmanalysis_off != True:
    # First, a word of caution
    print(' ###############################################\n',
          'WARNING 1: First analysis has finished. The program will\n',
          'now analyse asynchronous bpms, and after doing so it will\n',
          'overwrite the phase_output/, harmonic_output/ and temp/\n',
          'directories.\n',
          'If you require any of these, please save now, before\n',
          'continuing.\n',
          '\n',
          'WARNING 2: If you have switched on the flag "--plotbpma",\n',
          'and you are using a Windows machine, please ensure that\n',
          'you have an X server running, or launch the server the\n',
          'server now.\n',
          '###############################################\n',
          '\n')
    while True:
        user_input = raw_input('To continue, type "go". To abort type "quit".\n')
        if user_input == "go":
            print("Continuing...")
            break
        elif user_input == "quit":
            print("Quitting.")
            sys.exit()
            break
        else:
            print('Please enter a valid input (or try enclosing it in quotation marks).')
            continue

    for axis in ['x', 'y']:
        # async.py
        p = Popen([python_exe,
                   'async.py',
                   '--phase_output_dir', phase_output_dir,
                   '--async_output_dir', main_output_dir + 'outofphase' + axis + '/',
                   '--axis', axis])
        p.wait()
        
        if args.plotbpma == True:
            # checkBPMs_schematic.py
            p = Popen([python_exe,
                       'checkBPMs_schematic.py',
                       '--axis', axis,
                       '--sdds_dir', temp_dir,
                       '--async_output_dir', main_output_dir + 'outofphase' + axis + '/',
                       '--main_output_dir', main_output_dir,
                       '--when', 'before',
                       '--save'])
            p.wait()
    
            # checkBPMs_colormap.py
            p = Popen([python_exe,
                       'checkBPMs_colormap.py',
                       '--axis', axis,
                       '--sdds_dir', temp_dir,
                       '--phase_output_dir', phase_output_dir,
                       '--main_output_dir', main_output_dir,
                       '--when', 'before',
                       '--save'])
            p.wait()
    
    print(" ********************************************\n",
          "get_bpm_data.py:\n",
          '"Asynchronous BPMs found, converting raw -> sdds with synch fix."\n',
          "********************************************")
    
    # Conversion with asynch knowledge + KModu simulation
    file = open("run.sad", "w")
    file.write(' READ "' + lattice_dir + lattice_name + '";\n'
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
               ' fn1 = "' + ftwissbpm + '";\n'
               ' fn2 = "' + ftwissall + '";\n'
               ' SaveTwiss[fn1, fn2];\n\n'
               ' runs = Get["' + file_dict + '"];\n'
               ' Do[\n'
               '   fnr1 = "./"//runs[i, 1];\n'
               '   fbpm = "' + main_output_dir + 'outofphasex/"//runs[i, 2]//".txt";\n' # NOTE: outofphasex is used because it seems to have a cleaner output for resync.
               '   fwt1 = "' + temp_dir + '"//runs[i, 2];\n'
               '   FormatBPMRead[fnr1, fwt1, fbpm];\n'
               '   Print["Converting "//runs[i, 1]//" -> "//runs[i, 2]];\n'
               '   ,{i, 1, ' + loopend + '}];\n'
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
    
               ' abort;\n')
    file.close()
    
    os.system(gsad + " run.sad");
    print(" ********************************************\n",
          "get_bpm_data.py:\n",
          '"run.sad finished, running analysis script."\n',
          "********************************************")
    
    # Beta-Beat.src analysis
    p = Popen([python_exe,
               'run_BetaBeatsrc.py',
               '--python_exe', python_exe,
               '--BetaBeatsrc_dir', BetaBeatsrc_path,
               '--model_dir', model_dir,
               '--sdds_dir', temp_dir,
               '--harmonic_output_dir', harmonic_output_dir,
               '--phase_output_dir', phase_output_dir,
               '--mode', 'both'])
    p.wait()
    print(" ********************************************\n",
          "get_bpm_data.py:\n",
          '"Beta-Beat.src analysis finished, running async analysis again."\n',
          "********************************************")
    
    # Asynch analysis after
    # NOTE: This analysis is being run for both axes, but the x-axis is used
    #       in run.sad (generated below) as this one has been found to have 
    #       cleaner results.
    for axis in ['x', 'y']:
        # async.py
        p = Popen([python_exe,
                   'async.py',
                   '--phase_output_dir', phase_output_dir,
                   '--async_output_dir', main_output_dir + 'outofphase' + axis + '/',
                   '--axis', axis])
        p.wait()
    
        if args.plotbpma == True:
            # checkBPMs_schematic.py
            p = Popen([python_exe,
                       'checkBPMs_schematic.py',
                       '--axis', axis,
                       '--sdds_dir', temp_dir,
                       '--async_output_dir', main_output_dir + 'outofphase' + axis + '/',
                       '--main_output_dir', main_output_dir,
                       '--when', 'after',
                       '--save'])
            p.wait()
    
            # checkBPMs_colormap.py
            p = Popen([python_exe,
                       'checkBPMs_colormap.py',
                       '--axis', axis,
                       '--sdds_dir', temp_dir,
                       '--phase_output_dir', phase_output_dir,
                       '--main_output_dir', main_output_dir,
                       '--when', 'after',
                       '--save'])
            p.wait()

sys.exit()
