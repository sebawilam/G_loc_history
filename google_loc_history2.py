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
import easygui

from geopy.distance import geodesic
from geopy import Point
from geopy.geocoders import Nominatim

# %matplotlib inline

# input from the user
date_from = input('Date from, e.g. 2022-01-01: ')
date_to = input('Date to, e.g. 2022-01-31: ')
a = input('If address A/ If GPS location L: ')
if a.upper() == 'A':
    loc0 = input('Type address, e.g. Kolonia Zbyszkow 9C Grabow nad Pilica Poland: ')
else:
    loc2 = input('Type GPS coordinates, e.g (51.7343247, 21.2002061): ')

radius = int(input('Radius to consider on place: '))

# load the google location history data
file_dialog.fl_dialog()
file_path = easygui.fileopenbox("*.json","Load the google location history file", default="*.json") # , filetypes='*.json'
# df_gps = pd.read_json(file_dialog.file_path)
df_gps = pd.read_json(file_path)
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
# df_test = df_gps.iloc[1000:1005,:]
# df_test['timestamp'] = df_test['timestamp'].map(lambda x: x[:19])
# df_test['dtime'] = df_test['timestamp'].map(lambda x: dt.strptime(x, "%Y-%m-%dT%H:%M:%S"))
# df_test.dtypes

df_gps['timestamp'] = df_gps['timestamp'].map(lambda x: x[:19])
df_gps['dtime'] = df_gps['timestamp'].map(lambda x: dt.strptime(x, "%Y-%m-%dT%H:%M:%S"))

# print(df_gps.iloc[10000:10005,1:])
# print(df_gps.head())

df_2022 = df_gps[df_gps['dtime']>'2022-01-01']
df_gps = df_gps[df_gps['dtime']>=date_from]
df_gps = df_gps[df_gps['dtime']<=date_to]

if a.upper() == 'A':
    geolocator = Nominatim(user_agent="Python_Google_loc_history")
    location = geolocator.geocode(loc0)
    print(location.address)
    print((location.latitude, location.longitude))
    loc2 = (location.latitude, location.longitude)
# loc2 = (51.7343247, 21.2002061)
# loc2 = (51.7, 21.2)
# print(geodesic(loc1, loc2).m)
# df_2022['point'] = df_2022.apply(lambda x: Point(latitude=x['lat'], longitude=x['lon']), axis=1)
# df_2022['distance_km'] = df_2022.apply(lambda x: geodesic(x['point'], loc2).km, axis=1)
df_gps['point'] = df_gps.apply(lambda x: Point(latitude=x['lat'], longitude=x['lon']), axis=1)
df_gps['distance_km'] = df_gps.apply(lambda x: geodesic(x['point'], loc2).km, axis=1)

# df_2022['loc1'] = df_2022[['lat','lon']].values.tolist()
# df_2022['distance'] = geodesic(loc2,df_2022['loc1']).km

# df_2022['date'] = pd.to_datetime(df_2022['dtime']).dt.date
# print(max(df_2022['date']))
# # days_all = len(df_2022['date'])
# df_2022['on_place'] = df_2022['distance_km'].apply(lambda x: 'True' if x < 5 else 'False')
# df_2022_grp = df_2022.groupby('date')['on_place'].max()
# on_place_cnt = df_2022_grp.value_counts()
# print('All days: ' + str(on_place_cnt.sum()))
# print('On place days: ' + str(on_place_cnt['True']))
# print(str(on_place_cnt['True']/on_place_cnt.sum()*100) + '%')

df_gps['date'] = pd.to_datetime(df_gps['dtime']).dt.date
print(max(df_gps['date']))
# days_all = len(df_2022['date'])
df_gps['on_place'] = df_gps['distance_km'].apply(lambda x: 'True' if x < radius else 'False')
df_gps = df_gps.groupby('date')['on_place'].max()
on_place_cnt = df_gps.value_counts()
print('All days: ' + str(on_place_cnt.sum()))
print('On place days: ' + str(on_place_cnt['True']))
print(str(on_place_cnt['True']/on_place_cnt.sum()*100) + '%')
