import datetime as dt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def __extract_sequence__(df):
    df.drop('taxi', axis=1, inplace=True)
    df.sort_values(by='rebased_time', inplace=True)

    return df.values

def make_ready_for_ml(df, user_column='user', lat_column='latitude', lon_column='longitude', time_column='time'):
    df.reset_index(inplace=True)

    df['rebased_time'] = df[time_column] - df[time_column].min()
    df['rebased_time'] = df['rebased_time'].dt.total_seconds()

    scaler = StandardScaler()
    scaler.fit(df[[lon_column, lat_column, 'rebased_time']])
    df[[lon_column, lat_column, 'rebased_time']] = scaler.transform(df[[lon_column, lat_column, 'rebased_time']])

    df = df[[user_column, lon_column, lat_column, 'rebased_time']]
    df = df.groupby(user_column).apply(__extract_sequence__)

    return df, scaler