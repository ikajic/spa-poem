"""
This script reads the xls sheets contained in the `data_path` directory and
creates a dictionary with words as keys and a numpy array with 3 elements (EPA)
as values.

Two data sets are used: all sheets containing "AffectiveMeaningConcepts" are
part of one data set, and the sheet "EmotionFeatures_Fontaine" is part of
another data set. The Fontaine features are in a different space, so to be
converted to the EPA space the 2nd and 3rd dimension are scaled and inverted.
"""

import re
import os
import xlrd
import pickle
import sys
import numpy as np

# save pickled file
save = True

data_path = os.path.join(os.pardir, "data")  # source folder containing xls sheets

vocab = dict()        # vocabulary with concepts and epa values

# weighted average
wavg = lambda epam, epaf, nrm, nrf: (epam*nrm + epaf*nrf)/(nrm+nrf)

# chek if save the file
if len(sys.argv) != 1 and 'ns' in sys.argv[1]:
    print('Not saving...')
    save = False

# extract data from xls sheets
me, mp, ma = -1, -1, -1

nr_fontaine = 0     # number of words for which EPA was extracted
                    # from the Fontaine data set
nr_act = 0          # number of words from the other data set

for xls in os.listdir(data_path):
    if ("AffectiveMeaningsConcepts" not in xls) and ("Fontaine" not in xls):
        continue
    print('Processing:', xls)

    wb = xlrd.open_workbook(os.path.join(data_path, xls))
    sh = wb.sheet_by_index(0)

    for rownum in range(1, sh.nrows):
        row = sh.row_values(rownum)
        word = row[0].replace(' ', '_').upper()
        word = re.sub('[\W]+', '', word)

        if row.count('') != 0:
            continue

        if "Fontaine" in xls:
            nr_fontaine += 1
            epa = -4*np.array(row[2:5])  # scale and invert polarity
            epa[2] = -epa[2]
        else:
            nr_act += 1
            epa = wavg(np.array(row[1:4]), np.array(row[4:7]), row[7], row[8])

        vocab[word] = np.array([np.float(x) for x in epa])

print('Used Fontaine EPA profiles for %d words' % nr_fontaine)
print('Used ACT EPA profiles for %d words' % nr_act)

if save:
    name = 'epa_dimensions.pkl'
    file_savepath = os.path.join(data_path, name)
    with open(file_savepath, 'wb') as fpkl:
        pickle.dump(vocab, fpkl)

    print('Pickled file saved as: {}'.format(file_savepath))

    print('Testing opening')
    with open(file_savepath, 'rb') as fpkl:
        test = pickle.load(fpkl)
        print('Loaded {} entries'.format(len(test)))
