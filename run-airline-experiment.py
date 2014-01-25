import os
import glob
import shutil
import time
import cPickle

import numpy as np

import tools.split_data as split_data
import parallel_GPLVM

P = 60
Q = 9
num_inducing = 1000
path = './flight/'
dname = 'flight'

# 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 'DepTime', 'ArrTime', 'ArrDelay', 'AirTime', 'Distance', 'plane_age'

# First delete all current inputs & embeddings
split_data.clean_dir(path)

# Prepare directories
reqdirs = ['inputs', 'embeddings', 'tmp', 'proc']
for dirname in reqdirs:
    if not os.path.exists(path + '/' + dirname):
        os.mkdir(path + '/' + dirname)

# Load data
Y = np.load('./flight/proc/flight_regression_output.npy')
X = np.load('./flight/proc/flight_regression_inputs.npy')

perm = split_data.split_data(Y, P, path, dname)
split_data.split_embeddings(X, P, path, dname, perm)

# Run the Parallel GPLVM
options = {}
options['input'] = path + '/inputs/'
options['embeddings'] = path + '/embeddings/'
options['parallel'] = 'local'
options['iterations'] = 1000
options['statistics'] = path + '/tmp'
options['tmp'] = path + '/tmp'
options['M'] = num_inducing
options['Q'] = Q
options['D'] = 1
options['fixed_embeddings'] = True
options['keep'] = False
options['load'] = True
options['init'] = 'PCA'
options['optimiser'] = 'SCG_adapted'
options['fixed_beta'] = False

parallel_GPLVM.main(options)

# Copy output directory
shutil.copytree(path, '/scratch/mv310/results/' + dname + str(time.time()))
