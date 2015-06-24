#!/usr/bin/env python3

import sys, os
from os.path import basename, splitext
from matplotlib import pyplot as plt
import numpy as np

def run():
    # grab list of files from command line
    files = sorted(sys.argv[1:])

    # get a sorted list of files (using routine defined below)
    datasets = get_datasets(files)

    # averaging part
    n_ave = 2                   # edit this!
    for file_n in range(0, len(datasets) - n_ave + 1):
        # grab a subset
        sets = datasets[file_n:file_n+n_ave]

        # sum them, divide by the number
        file_sum = np.zeros(sets[0].shape)
        for dataset in sets:
            file_sum += dataset
        file_sum /= n_ave

        # plot the scatterplot
        plt.errorbar(file_sum[:,0], file_sum[:,1], yerr=file_sum[:,2])
        # zoom in
        plt.xlim(0, 100)

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


