"""
Created on Tue Jun 11
Author: Adam Koval
"""
from __future__ import print_function
import os
import argparse
import pandas
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from func import BPMs_from_sdds, get_all_outofsynch, get_dict_schematic

# Argument parser.
# TEMPORARY NOTE:
#   --axis <axis>
#   -aod outofphase + <axis> + /
#   -mod output/
#   -sd temp/
parser = argparse.ArgumentParser()
parser.add_argument('--axis', '-ax',
                    dest='axis',
                    action='store')
parser.add_argument('--async_output_dir', '-aod',
                    dest='async_output_dir',
                    action='store')
parser.add_argument('--main_output_dir', '-mod',
                    dest='main_output_dir',
                    action='store')
parser.add_argument('--sdds_dir', '-sd',
                    dest='sdds_dir',
                    action='store')
parser.add_argument('--save', '-s',
                    action='store_true')
args = parser.parse_args()

# List all BPMs from any sdds file.
BPM_list = BPMs_from_sdds(args.sdds_dir + os.listdir(args.sdds_dir)[0])[0]

# Get a dictionary of all files from outofsynch dir.
all_outofsynch = get_all_outofsynch(args.main_output_dir + args.async_output_dir)

# List all files in outofphase*/ dir.
file_list = os.listdir(args.main_output_dir + args.async_output_dir)

# Create dataframe for plotting.
df = {}
for file in file_list:
    df[file] = []
    for BPM in BPM_list:
        try:
            df[file].append(get_dict_schematic(all_outofsynch, file)[BPM])
        except KeyError:
            df[file].append('~')
df = pandas.DataFrame(df, index = BPM_list)

# Set up the plot.
column_length = len(df.columns.tolist())
row_length = len(BPM_list)
y_posn = [i for i in range(column_length)]
x_posn = [i for i in range(row_length)]

print("Ready to plot")

fig = plt.figure(figsize=(17, 11))
ax1 = fig.add_subplot(111)
plt.subplots_adjust(top=.84)
for i in range(column_length):
    for j in range(row_length):
        if df[file_list[i]][j] == '0':
            ax1.plot(x_posn[j], y_posn[i], 'o', color=[0., 1., .5], alpha=.5, label='no asynch')
        elif df[file_list[i]][j] == '-1':
            ax1.plot(x_posn[j], y_posn[i], 'o', color=[0., .5, 1.], alpha=.5, label='+1Q asynch')
        elif df[file_list[i]][j] == '+1':
            ax1.plot(x_posn[j], y_posn[i], 'o', color=[1., 0., 0.], alpha=.5, label='-1Q asynch')
        elif df[file_list[i]][j] == '~':
            ax1.plot(x_posn[j], y_posn[i], 'o', color=[.5, .5, .5], alpha=.5, label='no data')
    if i%3 == 0 and i != 0:
        print(str("{0:.1f}".format(i/column_length*100))+'%')
        ax1.axhline(y_posn[i]-.5, ls='--', lw=.5)

ax1.set_xticks([i for i in range(row_length)])
ax1.set_xticklabels(BPM_list, rotation='vertical')
ax1.set_yticks(y_posn)
ax1.set_yticklabels([i[:-4] for i in df.columns.tolist()])
ax1.set_ylabel('Measurement runs')
ax1.set_xlabel('BPM names')

custom_legend = [Line2D([0], [0], marker='o', color=[0., 1., .5], alpha=.5, label='no asynch'),
                 Line2D([0], [0], marker='o', color=[0., .5, 1.], alpha=.5, label='+1Q asynch'),
                 Line2D([0], [0], marker='o', color=[1., 0., 0.], alpha=.5, label='-1Q asynch'),
                 Line2D([0], [0], marker='o', color=[.5, .5, .5], alpha=.5, label='no data')]

ax1.legend(handles=custom_legend, bbox_to_anchor=(1, 1))
plt.title('Asynchronous BPMs in the ' + args.axis + '-axis from T-b-T data', y=1.02)

if args.save == True:
    plt.savefig('Asynchronous_BPMs_' + args.axis + 'axis.png', format='png')

plt.show()
