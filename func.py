from __future__ import print_function
import os
import re

# ====================================================
# To be used in get_bpm_data.py
# ====================================================
def look_for_dict():
    """
    Checks for the presence of the dict file.
    NOTE: This function does not check the format of the dictionary!
    """
    if os.path.exists('file_dict.txt'):
        print('Dictionary file has been found.')
        return True
    else:
        print('You have not provided a dictionary file.')
        return False


def read_pathnames():
    """
    Reads specifically the file 'pathnames.txt'
    and returns a dictionary with the assigned values.
    """
    with open('pathnames.txt') as f:
        lines = f.readlines()
    lines = [line for line in lines if line[0] != '#']

    pathnames = {}
    for line in lines:
        line = line.split()
        pathnames[line[0]] = line[-1]

    return pathnames


def generic_dict(data_input_dir, ringID):
    """
    Creates a generic file_dict.txt file given
    only the input data files and the ring for which one
    wishes to create a file_dict.txt.
    """
    files = []
    for file in os.listdir(data_input_dir):
        if file.endswith('.data') and file.startswith(ringID):
            files.append(file)

    fd = open('file_dict.txt', 'w')
    fd.write('{\n')
    for i, file in enumerate(files):
        before = data_input_dir + file
        after = file[:-5] + '.sdds'
        if files[i] != files[-1]:
            fd.write('    {"' + before + '", "' + after + '"},\n')
        else:
            fd.write('    {"' + before + '", "' + after + '"}\n')
    fd.write('}\n')
    fd.close()


# ====================================================
# To be used in async.py
# ====================================================
def phase(datapath, axis):
    """
    Reads getphase*.out and returns required columns as arrays.
    """
    with open(datapath + 'getphase' + axis + '.out') as f:
        lines=f.readlines()
    S1 = [float(lines[10+i].split()[0]) for i in range(len(lines[10:]))]
    S2 = [float(lines[10+i].split()[4]) for i in range(len(lines[10:]))]
    Sall = np.hstack([S1, S2[-1]])
    name1 = [lines[10+i].split()[2] for i in range(len(lines[10:]))]
    name2 = [lines[10+i].split()[3] for i in range(len(lines[10:]))]
    namesall = np.hstack([name1, name2[-1]])
    deltaph = [float(lines[10+i].split()[-1]) for i in range(len(lines[10:]))]
    phx = [float(lines[10+i].split()[-2]) for i in range(len(lines[10:]))]
    phxmdl = [float(lines[10+i].split()[-4]) for i in range(len(lines[10:]))]
    Qx = float(lines[5].split()[3])
    Qy = float(lines[6].split()[3])
    return Sall, namesall, deltaph, phx, phxmdl, Qx, Qy


def phasetot(datapath, axis):
    """
    Reads getphasetot*.out and returns deltaphtot array.
    """
    with open(datapath + 'getphasetot' + axis + '.out') as f:
        lines = f.readlines()[8:]
    deltaphtot = [float(lines[2+i].split()[-1]) for i in range(len(lines[2:]))]
    return deltaphtot


# ====================================================
# To be used in checkBPMs*.py
# ====================================================
def BPMs_from_sdds(sddsfile):
    """
    Finds the complete list of BPMs from the sdds file.
    """
    with open(sddsfile) as f:
        lines = f.readlines()
    lines = [line for line in lines if not line.startswith('#')]

    BPMs = []
    badBPMs = []
    for line in lines:
        if line.startswith('0'):
            BPMs.append(line.split()[1])
            if line.split()[3] == '.0000000000':
                badBPMs.append(line.split()[1])

    return BPMs, badBPMs


def get_all_outofsynch(async_output_dir):
    """
    Creates a dictionary with keys corresponding to the
    <run>.txt filename of the measurement run, as
    given in file_dict.txt, and each entry containing
    the list of BPMs along with their integer
    out-of-synch values, as stated in the respective
    outofsynch/<file>.txt file.
    """
    files = os.listdir(async_output_dir)
    all_outofsynch = {}
    for i, fn in enumerate(files):
        with open(async_output_dir + fn) as f:
            column = f.readlines()
        del column[-1]
        del column[0]
        all_outofsynch[files[i]] = column
    return all_outofsynch


def get_dict_schematic(dictionary, file):
    """
    For the file with name <file>, returns a dictionary
    of keys corresponding to each BPM in that file, and
    key entries consisting of the status of that BPM as
    a string:
    '+1', '0' or '-1'.
    """
    def get_info(pattern):
        info = []
        for key_entry in dictionary[file]:
            info.append(re.search(pattern, key_entry).group(1))
        return info
    names = get_info('\"([A-Z0-9]+)\"\S*')
    asynchs = get_info('\-\>([\+\-]*[0-9])')
    Dict = {}
    for i in range(len(names)):
        Dict[names[i]] = asynchs[i]
    return Dict


def get_dict_colormap(names, phases):
    """
    Given an array of BPM names and their respective
    phases, returns a dictionary with BPM name keys
    and phase advance entries.
    """
    Dict = {}
    for i in range(len(names)):
        Dict[names[i]] = phases[i]
    return Dict


def get_data_column(phase_output_dir, folder, data, column):
    """
    Obtain desired data column from measurement run in phase
    output dir as an array.
    """
    with open(phase_output_dir + folder + '/' + data) as f:
        lines = f.readlines()
    rows = [line for line in lines if line.split()[0] not in ['@', '*', '$']]
    headers, = [line for line in lines if line.split()[0] == '*']
    headers = headers.split()[1:]
    all_dat = {}
    for i in range(len(headers)):
        if headers[i] in ['NAME', 'NAME2']:
            all_dat[headers[i]] = [rows[j].split()[i] for j in range(len(rows))]
        else:
            all_dat[headers[i]] = [float(rows[j].split()[i]) for j in range(len(rows))]
    return all_dat[column]
