import cartopy.crs as ccrs
import datetime as dt
import numpy as np
import pandas as pd
import sys

name = sys.argv[1]

print('Reading data from generated csv file ...')

# Read data from generated file
df = pd.read_csv('trips_%s.csv' % (name))

# Rename, delete etc. columns in order to achieve the 'standard' format
df['user'] = df['Moid']
df['time'] = pd.to_datetime(df['Tstart'], format = '%Y-%m-%d %H:%M:%S')
df['trip'] = df['Tripid']

#print(ccrs.PlateCarree().transform_points(ccrs.UTM(10), df['Xstart'].values, df['Ystart'].values))
a = ccrs.PlateCarree().transform_points(ccrs.UTM(10), df['Ystart'].values, df['Xstart'].values)
df['longitude'] = a[:, 0]
df['latitude'] = a[:, 1]

df.drop(['Moid', 'Tstart', 'Tend', 'Xstart', 'Xend', 'Ystart', 'Yend', 'Tripid'], axis=1, inplace=True)

print('Changing the way the dataset is indexed ...')

# Change the way the dataset is indexed
df_reindexed = df.set_index(['user', 'time'])
df_reindexed.sort_index(inplace=True)

print('Saving the dataset to .pkl ...')

# Save the dataset to .pkl
df_reindexed.to_pickle('trips_%s.pkl' %(name))

print('...done!')