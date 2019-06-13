"""
Created on Tue Jun 11
Author: Adam Koval
"""
from __future__ import print_function
import os
import sys
import argparse
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from func import BPMs_from_sdds, get_data_column, get_dict_colormap

# Argument parser.
parser = argparse.ArgumentParser()
parser.add_argument('--axis', '-ax',
                    dest='axis',
                    action='store')
parser.add_argument('--phase_output_dir', '-pod',
                    dest='phase_output_dir',
                    action='store')
parser.add_argument('--main_output_dir', '-mod',
                    dest='main_output_dir',
                    action='store')
parser.add_argument('--sdds_dir', '-sd',
                    dest='sdds_dir',
                    action='store')
parser.add_argument('--display', '-d',
                    action='store_true')
parser.add_argument('--save', '-s',
                    action='store_true')
args = parser.parse_args()

# Definitions.
axis = args.axis
AXIS = axis.capitalize()
sdds_dir = args.sdds_dir
phase_output_dir = args.phase_output_dir
main_output_dir = args.main_output_dir
data = 'getphasetot' + axis + '.out'

# List all files in phase_output_dir.
file_list = os.listdir(phase_output_dir)

# List all BPMs from any sdds file.
BPM_list = BPMs_from_sdds(sdds_dir + os.listdir(sdds_dir)[0])[0]

# Create dataframe for plotting.
df = {}
for file in file_list:
    df[file] = []
    names = get_data_column(phase_output_dir, file, data, 'NAME')
    phases = get_data_column(phase_output_dir, file, data, 'DELTAPHASE' + AXIS)
    for BPM in BPM_list:
        try:
            df[file].append(get_dict_colormap(names, phases)[BPM])
        except KeyError:
            df[file].append(np.nan)
df = pandas.DataFrame(df, index=BPM_list)
df = df

# Set up the plot.
with open('cmap.txt','r') as f:
    lines = f.readlines()
cmatrix = []
for i in range(len(lines)):
    cmatrix.append([float(j)/255.0 for j in lines[i].split()])
cm = colors.ListedColormap(cmatrix)

X, Y = np.meshgrid(
    np.linspace(
        0, len(BPM_list), len(BPM_list) + 1),
    np.linspace(
        0, len(file_list), len(file_list) + 1))
Z = df.T

column_length = len(df.columns.tolist())
row_length = len(BPM_list)
y_posn = [i for i in range(column_length)]
x_posn = [i for i in range(row_length)]

# Plot.
fig = plt.figure(figsize=(17, 11))
ax = fig.add_subplot(111)

plt.pcolormesh(X, Y, Z, cmap = cm)
bar = plt.colorbar()
bar.set_label('$\Delta\ \phi$ [2$\pi$]')

for i in range(column_length):
    if i%3 == 0 and i != 0:
        ax.axhline(y_posn[i], ls='--', lw=1)

ax.set_xticks([i for i in range(row_length)])
ax.set_xticklabels(BPM_list, rotation='vertical')
ax.set_yticks([i+.5 for i in y_posn])
ax.set_yticklabels([i[:-4] for i in df.columns.tolist()])
ax.set_xlabel('BPM')
ax.set_ylabel('Measurement run')
plt.title('SuperKEKB BPM performance from T-b-T data (' + axis + '-axis)')

if args.save == True:
    plt.savefig(main_output_dir + 'colourmap_Asynchronous_BPMs_' + axis + 'axis.png', format = 'png')
if args.sidplay == True:
    plt.show()

print(" *******************************\n",
      "checkBPMs_colormap.py: Script made it to the end, moving on...\n",
      "*******************************")

sys.exit()
