import datetime as dt
import numpy as np
import pandas as pd
import sys

name = sys.argv[1]

print('Reading data from generated csv file ...')

# Read data from generated file
df = pd.read_csv('berlinmod/trips_%s.csv' % (name))
df['time'] = pd.to_datetime(df['Tstart'], format = '%Y-%m-%d %H:%M:%S')
df['longitude'] = df['Xstart']
df['latitude'] = df['Ystart']
df['trip'] = df['Tripid']
df.drop(['Tstart', 'Tend', 'Xstart', 'Xend', 'Ystart', 'Yend', 'Tripid'], axis=1, inplace=True)

print('Changing the way the dataset is indexed ...')

# Change the way the dataset is indexed
df_reindexed = df.set_index(['Moid', 'time'])
df_reindexed.sort_index(inplace=True)

print('Saving the dataset to .pkl ...')

# Save the dataset to .pkl
df_reindexed.to_pickle('berlinmod/%s.pkl' %(name))

print('...done!')