import sys
import pandas as pd

raw_path = sys.argv[1]
print('Reading file \'{}\' ...'.format(raw_path))
df = pd.read_pickle(raw_path)

print('Reindexing ...')
df.reset_index(inplace=True)

def __extract_sequence__(df):
    df.drop('user', axis=1, inplace=True)
    df.sort_values(by='time', inplace=True)

    return df.values

print('Reshaping the DataFrame ...')
df = df[['user', 'longitude', 'latitude', 'time']]
df = df.groupby('user').apply(__extract_sequence__)

reshaped_path = raw_path[:-4] + '_mlshaped.pkl'
print('Writing file \'{}\' ...'.format(reshaped_path))
df.to_pickle(reshaped_path)