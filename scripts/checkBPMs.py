#!/afs/cern.ch/work/o/omc/anaconda3/bin/python3
import os
import re
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

### README ####
# sys.argv[1] == 'x','y'
# sys.argv[2] == 'plot'

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def my_max(listoflists):
    current_max_len = len(listoflists[0][0])
    for x in listoflists:
        if len(x[0]) > current_max_len:
            current_max_len = len(x[0])
            current_max_list = x[0]
            current_max_file = x[1]
        else:
            pass
    return current_max_list, current_max_file

def get_names(dictionary, filelist, k):
    return [re.search("\"([A-Z0-9]+)\"\S*", dictionary[filelist[k]][i]).group(1) for i in range(len(dictionary[filelist[k]]))], filelist[k]

def get_asynchs(dictionary, filelist, k):
    return [re.search("\-\>([\+\-]*[0-9])", dictionary[filelist[k]][i]).group(1) for i in range(len(dictionary[filelist[k]]))]

def get_dict(dictionary, filelist, k):
    names = get_names(dictionary, filelist, k)[0]
    asynchs = get_asynchs(dictionary, filelist, k)
    return {names[i]:asynchs[i] for i in range(len(names))}

def list_and_except(dictionary, filelist, nameslist, i):
    List = []
    for k in range(len(filelist)):
        try:
            List.append(get_dict(dictionary, filelist, k)[nameslist[i]])
        except KeyError:
            List.append('~')
    return List

def get_S(file, path, axis):
    with open(path+file+'sdds/getphase'+axis+'.out') as f:
        lines = f.readlines()[10:]
    S = []
    S.append('0')
    for i in range(len(lines)):
        S.append(lines[i].split()[0])
    return S

axis = sys.argv[1]

if axis == 'x':
    pathtoFile = 'outofphasex'
elif axis == 'y':
    pathtoFile = 'outofphasey'

pathforS = 'unsynched_phase_output/'

g = 0
filesList = sorted([i for i in listdir_nohidden(pathtoFile)])
rawData = {}

for File in filesList:
    with open(pathtoFile+'/'+File) as f:
        column = f.readlines()
        del column[-1]; del column[0]
        rawData[filesList[g]] = column
    g += 1

longestNamesList = [i[:-1] for i in open('BPMlist.txt','r').readlines()]

datall = {}
for i in range(len(longestNamesList)):
    datall[longestNamesList[i]] = list_and_except(rawData, filesList, longestNamesList, i)

df = pd.DataFrame(datall, index = filesList)
df = df.T
if axis == 'x':
    df.to_csv('FaultyBPMSx.csv')
elif axis == 'y':
    df.to_csv('FaultyBPMSy.csv')

column_length = len(df.columns.tolist())
row_length = len(longestNamesList)
y_posn = [i for i in range(column_length)]
x_posn = [i for i in range(row_length)]

print('Ready to plot')

try:
    if sys.argv[2] == 'plot':
        fig = plt.figure(figsize = (17,11))
        ax1 = fig.add_subplot(111)
        plt.subplots_adjust(top = .84)

        for i in range(column_length):
            for j in range(row_length):
                if df[filesList[i]][j] == '0':
                    ax1.plot(x_posn[j], y_posn[i],'o', color = [0,1,.5], alpha = .5, label = 'no asynch')
                elif df[filesList[i]][j] == '-1':
                    ax1.plot(x_posn[j], y_posn[i],'o', color = [0,.5,1], alpha = .5, label = '+1Q asynch')
                elif df[filesList[i]][j] == '+1':
                    ax1.plot(x_posn[j], y_posn[i],'o', color = [1,0,0], alpha = .5, label = '-1Q asynch')
                elif df[filesList[i]][j] == '~':
                    ax1.plot(x_posn[j], y_posn[i],'o', color = [.5,.5,.5], alpha = .5, label = 'no data')
            if i%3 == 0 and i != 0:
                print(str("{0:.1f}".format(i/column_length*100))+'%')
                ax1.axhline(y_posn[i]-.5, ls = '--', lw = .5)

        ax1.set_xticks([i for i in range(row_length)])
        ax1.set_xticklabels(longestNamesList, rotation = 'vertical')
        ax1.set_yticks(y_posn)
        ax1.set_yticklabels([i[:-4] for i in df.columns.tolist()])
        ax1.set_ylabel('Measurement runs')
        ax1.set_xlabel('BPM name')

        custom_legend = [Line2D([0], [0], marker = 'o', color = [0,1,.5], alpha = .5, label = 'no asynch'),
                         Line2D([0], [0], marker = 'o', color = [0,.5,1], alpha = .5, label = '+1Q asynch'),
                         Line2D([0], [0], marker = 'o', color = [1,0,0], alpha = .5, label = '-1Q asynch'),
                         Line2D([0], [0], marker = 'o', color = [.5,.5,.5], alpha = .5, label = 'no data')]
        ax1.legend(handles = custom_legend, bbox_to_anchor=(1, 1))

        plt.title('Asynchronous BPMs in the '+axis+'-axis from T-b-T data', y = 1.02)

        try:
            if sys.argv[3] == 'save':
                plt.savefig('Asynchronous_BPMs_'+axis+'axis.png',format='png')
        except IndexError:
            pass
        print('Ready to view')
        plt.show()
except IndexError:
    pass
