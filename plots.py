#!/usr/bin/env python3
"""
plotting script.
 - first argument is the file listing inputs,
 - second argument is the number of files to average
"""
import sys, os
from os.path import basename, splitext
from matplotlib import pyplot as plt
import numpy as np



def run():
    # grab list of files from command line
    files = []
    for line in open(sys.argv[1]):
        stripped_line = line.strip()
        if not stripped_line:
            continue
        files.append(stripped_line)
    n_ave = int(sys.argv[2])

    # get a sorted list of files (using routine defined below)
    datasets = get_datasets(files)

    # averaging part
    for file_n in range(0, len(datasets) - n_ave + 1):
        # grab a subset
        sets = datasets[file_n:file_n+n_ave]

        # sum them, divide by the number
        n_entries = sets[0].shape[0]
        x_vals = sets[0][:,0]
        y_num, y_denom = np.zeros(n_entries), np.zeros(n_entries)
        for dataset in sets:
            # get x, y, and z for this dataset
            x, y, sigma = [x.flatten() for x in np.split(dataset, 3, axis=1)]
            assert np.all(np.isclose(x, x_vals)), (x, x_vals)

            # THIS IS WHERE ALL THE LOGIC with averaging points is
            # only add the valid points: `vp` is an array pointing to them
            vp = (sigma != 0)

            vy, vs = y[vp], sigma[vp]
            y_num[vp] += vy / vs**2
            y_denom[vp] += 1 / vs**2

        # redefine valid points to be all points where something has been
        # added
        vp = (y_denom != 0)
        y_vals = y_num[vp] / y_denom[vp]
        # print(y_vals, y_num, y_denom)
        error_bars = 1/(y_denom[vp])**0.5

        # plot the scatterplot
        plt.errorbar(x_vals[vp], y_vals, yerr=error_bars)

        # zoom in, label things
        plt.xlim(0, 100)
        plt.xlabel('something on x')
        plt.ylabel('something on y')

        # get the file names (use the 'stub' function below)
        name1, name2 = stub(files[file_n]), stub(files[file_n + n_ave - 1])

        # compose the output name
        fig_name = 'fig_{}_to_{}.pdf'.format(name1, name2)

        # save and close
        print('saving {}'.format(fig_name))
        plt.savefig(fig_name)
        plt.clf()

def stub(long_name):
    """short function to make short name for the output"""
    return basename(splitext(long_name)[0])

def get_datasets(files):
    """function to get a list of datasets as arrays"""
    # read in the datasets, they will be stored as numpy arrays
    datasets = []
    for dat_path in files:

        # open the file
        dat = open(dat_path)

        # make an empyt list, we'll append the data in the file to this
        datalist = []
        # loop over the lines in the file
        for line in dat:
            entries = line.split()

            # skip lines without three numbers
            if len(entries) != 3:
                continue

            # convert the entries from text to floats
            entries_as_float = [float(x) for x in entries]

            datalist.append(entries_as_float)
        datasets.append(np.array(datalist))
    return datasets

# call run function
if __name__ == '__main__':
    run()


