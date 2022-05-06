# -*- coding: utf-8 -*-
"""
Created on Thu May  5 22:15:33 2022

@author: Seba
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from time import gmtime, strftime
strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

# from mpl_toolkits.basemap import Basemap
import file_dialog
# %matplotlib inline

# load the google location history data
file_dialog.fl_dialog()
df_gps = pd.read_json(file_dialog.file_path)
print('There are {:,} rows in the location history dataset'.format(len(df_gps)))

# parse lat, lon, and timestamp from the dict inside the locations column
df_gps['lat'] = df_gps['locations'].map(lambda x: x['latitudeE7'])
df_gps['lon'] = df_gps['locations'].map(lambda x: x['longitudeE7'])
# df_gps['timestamp_ms'] = df_gps['locations'].map(lambda x: x['timestamp'])
df_gps['timestamp'] = df_gps['locations'].map(lambda x: x['timestamp'])
df_gps['accuracy'] = df_gps['locations'].map(lambda x: x['accuracy'])
df_gps['source'] = df_gps['locations'].map(lambda x: x['source'])
# df_gps['activity'] = df_gps['locations'].map(lambda x: x['activity'])

# convert lat/lon to decimalized degrees and the timestamp to date-time
df_gps['lat'] = df_gps['lat'] / 10.**7
df_gps['lon'] = df_gps['lon'] / 10.**7
# date_range = '{}-{}'.format(df_gps['datetime'].min()[:4], df_gps['datetime'].max()[:4])
# df_gps['timestamp_dt'] = dt.fromtimestamp(df_gps['timestamp'].seconds + df_gps['timestamp'].nanos/1e9)

# drop columns we don't need, then show a slice of the dataframe
# df_gps = df_gps.drop(labels=['locations', 'timestamp_ms'], axis=1, inplace=False)
df_test = df_gps.iloc[1000:1005,:]
df_test['timestamp'] = df_test['timestamp'].map(lambda x: x[:19])
df_test['dtime'] = df_test['timestamp'].map(lambda x: dt.strptime(x, "%Y-%m-%dT%H:%M:%S"))

df_gps['timestamp'] = df_gps['timestamp'].map(lambda x: x[:19])
df_gps['dtime'] = df_gps['timestamp'].map(lambda x: dt.strptime(x, "%Y-%m-%dT%H:%M:%S"))

print(df_gps.iloc[10000:10005,1:])
print(df_gps.head())
