import datetime as dt
import numpy as np
import pandas as pd

def __extract_sequence__(df):
    df.drop('user', axis=1, inplace=True)
    return df.values

# Converts a records Pandas Dataframe in my standard format to a Pandas Series
# that maps users to their entires geolocation data.
def records_to_user_geolcation(records):
    records.reset_index(inplace=True)

    # Compute timestamp in seconds since earliest timestamp
    records['rebased_time'] = records['time'] - records['time'].min()
    records['rebased_time'] = records['rebased_time'].dt.total_seconds()

    # Limit the dataframe to the needed columns
    records = records[['user', 'rebased_time', 'longitude', 'latitude']]

    # Create a new dataframe of users to their geolocation data from the records dataframe
    user_geolocation = records.groupby('user').sort_values(by='rebased_time').apply(__extract_sequence__)

    return user_geolocation

# Like records_to_user_geolcation but time stamps are deltas to previous
def records_to_user_geolcation_2(records):
    records.reset_index(inplace=True)

    # Compute delta time stamps in seconds since previous record
    records['delta_time'] = records.sort_values(by='time').groupby('user')['time'].diff().dt.total_seconds()
    records['delta_time'] = records['delta_time'].fillna(0)
    
    # Limit the dataframe to the needed columns
    records = records[['user', 'delta_time', 'longitude', 'latitude']]

    # Create a new dataframe of users to their geolocation data from the records dataframe
    user_geolocation = records.groupby('user').apply(__extract_sequence__)

    return user_geolocation

# Converts a Pandas Series to a Numpy array of all users' geolocation data
# concatenated.
def user_geolocation_to_single_sequence(user_geolocation):
    seq = None
    for _, item in user_geolocation.iteritems():
        if seq is None:
            seq = item
        else:
            seq = np.concatenate((seq, item), axis=0)
    
    return seq

def __reshape_to_feed_order__(data, n_batches, sequence_length):
    tmp = data[:, :sequence_length]
    for b in range(1, n_batches):
        tmp = np.concatenate([tmp, data[:, b * sequence_length:(b + 1) * sequence_length]])
    data = tmp

    return data

# Reshapes a Numpy array of concatenated geolocation data sequences to a Numpy
# array of sequenes that are sequence_length long. The succeeding sequence to
# any one sequence is placed batch_size rows later, so this Numpy array can be
# fed into the Keras's Model.fit function of a stateful model and the state is
# correctly applied.
# This function also returns the corresponding targets to the data as well as
# the computed number of batches.
def reshape_single_sequence_to_rnn_Xy(seq, batch_size, sequence_length):
    n_batches = (seq.shape[0] - 1) // (batch_size * sequence_length)
    rounded_length = n_batches * batch_size * sequence_length

    X = seq[:rounded_length].reshape([batch_size, n_batches * sequence_length, 3])
    y = seq[1:rounded_length + 1].reshape([batch_size, n_batches * sequence_length, 3])

    X = __reshape_to_feed_order__(X, n_batches, sequence_length)
    y = __reshape_to_feed_order__(y, n_batches, sequence_length)

    return n_batches, X, y