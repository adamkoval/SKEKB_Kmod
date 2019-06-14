#!/afs/cern.ch/work/o/omc/anaconda3/bin/python3
import os
import re
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
def my_max(dictoflists):

    first_key = list(dictoflists.keys())[0]
    current_max_len = len(dictoflists[first_key])
    current_max_list = dictoflists[first_key]
    current_max_folder = first_key

    for x in dictoflists:
        if len(dictoflists[x]) > current_max_len:
            current_max_len = len(dictoflists[x])
            current_max_list = dictoflists[x]
            current_max_folder = x
        else:
            pass

    return current_max_list, current_max_folder


def get_data(path, folder, data, column):

    with open(path + '/' + folder + '/' + data) as f:
        all_lines = f.readlines()

    rows = [line for line in all_lines if line.split()[0] not in ['@', '*', '$']]
    headers, = [line for line in all_lines if line.split()[0] == '*']
    headers = headers.split()[1:]

    all_dat = {}
    for i in range(len(headers)):
        if headers[i] in ['NAME', 'NAME2']:
            all_dat[headers[i]] = [rows[j].split()[i] for j in range(len(rows))]
        else:
            all_dat[headers[i]] = [float(rows[j].split()[i]) for j in range(len(rows))]

    return all_dat[column]


def get_all_Ss(path, data):

    folders_list = [folder for folder in os.listdir(path) if folder[-4:] == 'sdds']

    S_dict = {}
    for i in range(len(folders_list)):
        S_dict[folders_list[i]] = get_data(path, folders_list[i], data, 'S')

    return S_dict

def note_missing_data(path, folder, data, datum):
    longest_S_folder = my_max(get_all_Ss(path,data))[1]
    longest_NAMEs = get_data(path, longest_S_folder, data, 'NAME')

    current_NAMEs = get_data(path, folder, data, 'NAME')
    current_data = get_data(path, folder, data, datum)
    current_dict = {current_NAMEs[i]:current_data[i] for i in range(len(current_NAMEs))}

    prepared_dict = {}
    for k in range(len(longest_NAMEs)):
        try:
            prepared_dict[longest_NAMEs[k]] = current_dict[longest_NAMEs[k]]
        except KeyError:
            prepared_dict[longest_NAMEs[k]] = np.nan

    return prepared_dict

def data_from_dict(dictionary):
    just_a_list = []
    for k in dicitonary:
        just_a_list.append(dictionary[k])
    return just_a_list

if __name__ == "__main__":

    path = 'unsynched_phase_output'
    axis = sys.argv[1]
    if axis == 'x':
        AXIS = 'X'
    elif axis == 'y':
        AXIS = 'Y'
    folders = sorted([folder for folder in os.listdir(path) if folder[-4:] == 'sdds'])
    data = 'getphasetot' + axis + '.out'

    longest_S, longest_S_folder = my_max(get_all_Ss(path, data))
    longest_NAMEs = get_data(path, longest_S_folder, data, 'NAME')

    f = open('missingBPM'+axis+'.txt','w')
    for i in range(len(folders)):
        prepped_datum = note_missing_data(path, folders[i], data, 'DELTAPHASE'+AXIS) 
        f.write(folders[i]+' :::\t')
        [f.write(key+'\t') for key in prepped_datum if np.isnan(prepped_datum[key]) == True]
        f.write('\n\n')
        print(str(i)+'/'+str(len(folders)))
    f.close()

    DELTAPHASEs = {}
    for i in range(len(folders)):
        prepped_data = note_missing_data(path, folders[i], data, 'DELTAPHASE'+AXIS)
        DELTAPHASEs[folders[i]] = [prepped_data[k] for k in prepped_data]
    DELTAPHASEs_array = np.array([DELTAPHASEs[k] for k in DELTAPHASEs])

    with open('cmap.txt','r') as f:
        lines = f.readlines()
    cmatrix = []
    for i in range(len(lines)):
        cmatrix.append([float(j)/255.0 for j in lines[i].split()])
    cm = colors.ListedColormap(cmatrix)

    fig = plt.figure()
    X, Y = np.meshgrid(longest_S + [longest_S[-1]], np.linspace(0, len(folders), len(folders) + 1))
#    X, Y = np.meshgrid(np.linspace(0,len(longest_S), len(longest_S) + 1), np.linspace(0, len(folders), len(folders) + 1))
    Z = DELTAPHASEs_array
    plt.pcolormesh(X, Y, Z, cmap = cm)
    bar = plt.colorbar()
    bar.set_label('$\Delta\ \phi$ [2$\pi$]')
    plt.xlabel('S [m]')
    plt.ylabel('Measurement run [in groups of 3]')
    plt.yticks([i for i in range(len(folders)) if i%3 == 0])
    plt.title('SuperKEKB BPM performance from T-b-T data ('+axis+'-axis)')
    plt.savefig('colourmap_Asynchronous_BPMs_'+axis+'axis.png', format = 'png')
    plt.show()
