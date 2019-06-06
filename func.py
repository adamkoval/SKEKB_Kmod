from __future__ import print_function
import os
import re

def look_for_dict(init_path):
    """
    Function which checks for the presence of the dict file.
    NOTE: This function does not check the format of the dictionary!
    """
    if os.path.exists(init_path + 'file_dict.txt'):
        print('Dictionary file has been found.')
        return True
    else:
        print('You have not provided a dictionary file.')
        return False


def read_pathnames():
    """
    This function reads specifically the file 'pathnames.txt'
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


def generic_dict(data_input_dir, ringID, init_path):
    """
    Function for creating a generic file_dict.txt file given
    only the input data files and the ring for which one
    wishes to create a file_dict.txt.
    """
    files = []
    for file in os.listdir(data_input_dir):
        if file.endswith('.data') and file.startswith(ringID):
            files.append(file)

    fd = open(init_path + 'file_dict.txt', 'w')
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
