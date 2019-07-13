import os
import sys
import re
import numpy as np

sdds_dir = 'temp_current'
harmonic_path = 'output_current/harmonic_output/'
files = os.listdir(sdds_dir)

# Extract tunes
tunes = {}
Qxs = []
Qys = []
for file in files:
    for axis in ['x', 'y']:
        try:
            with open(harmonic_path + file + '.lin' + axis) as f:
                lines = f.readlines()
                globals()['Q' + axis + 's'].append(float(lines[0].split()[3]))
        except IOError:
            pass

# Extract info from file names
Magnets = [re.search('([A-Z0-9]+)\_[-+]*[0-9]+\_[0-9a-z-]*\_[0-9]\.sdds', file).group(1) for file in files]
RFs = [float(re.search('[A-Z0-9]+\_([-+]*[0-9]+)\_[0-9a-z-]*\_[0-9]\.sdds', file).group(1)) for file in files]
dKs = [float(re.search('[A-Z0-9]+\_[-+]*[0-9]+\_([0-9a-z-]*)\_[0-9]\.sdds', file).group(1)) for file in files]

# This is a test
testarr = []
testvar = Qxs
for i in range(len(testvar)):
    if Magnets[i] == 'QC1RE':
        if RFs[i] == 200.0:
            if dKs[i] == -0.0002:
                testarr.append(testvar[i])
                print(testvar[i])

# Back to business
Magnets = [k for i, k in enumerate(Magnets) if (i+1)%5==0]
RFs = [k for i, k in enumerate(RFs) if (i+1)%5==0]
dKs = [k for i, k in enumerate(dKs) if (i+1)%5==0]

# Find average tune for each setting and find std error
avgQxs = []
avgQys = []
Qx_errs = []
Qy_errs = []
for i in range(len(Magnets)):
    Qx_subset = [Qxs[k] for k in range(i*5, (i+1)*5)]
    Qy_subset = [Qys[k] for k in range(i*5, (i+1)*5)]
    Qx_errs.append(np.std(Qx_subset))
    Qy_errs.append(np.std(Qy_subset))
    avgQxs.append(np.average(Qx_subset))
    avgQys.append(np.average(Qy_subset))

fn = 'tunes_test.txt'
f = open(fn, 'w')
f.write('Magnet\t\tdF[Hz]\t\tdK/k\t\tnux\t\t\tnux_std\t\t\tnuy\t\t\tnuy_std\n')
for i in range(len(avgQxs)):
    f.write(Magnets[i] + '\t\t'
            + str(RFs[i]) + '\t\t'
            + str(dKs[i]) + '\t\t'
            + str(avgQxs[i]) + '\t'
            + str(Qx_errs[i]) + '\t'
            + str(avgQys[i]) + '\t'
            + str(Qy_errs[i]) + '\n')
f.close()
