import pandas as pd
import os
import numpy as np

df = pd.read_csv('AllStats.csv')
df['SHOT_MADE_STRING'] = df['SHOT_MADE_FLAG'].astype(str)
df['shot_count'] = df.groupby('PLAYER_ID')['PLAYER_ID'].transform('count')

df = df[df['shot_count'] > 100]
df = df[df['LOC_Y'] < 420]
df = df.sort_values(by='shot_count', ascending=False)
df['dates'] = pd.to_datetime(df['GAME_DATE'], format='%Y%m%d')
df['dates'] = df['dates'].astype(str)

df['GAME_NAME'] = df['HTM'] + ' @ ' + df['VTM'] + ' ' + df['dates']

conditions = [
    (df['SHOT_TYPE'] == '3PT Field Goal') & (df['SHOT_MADE_FLAG'] == 1),
    (df['SHOT_TYPE'] == '2PT Field Goal') & (df['SHOT_MADE_FLAG'] == 1),
    (df['SHOT_MADE_FLAG'] == 0)]
choices = [3, 2, 0]
df['points'] = np.select(conditions, choices)

df['gamepoints'] = df.groupby(['PLAYER_ID', 'GAME_ID'])['points'].transform('sum')
df['gamepoints'] = df['gamepoints'].astype(str)

df['GAME_NAME'] = df['HTM'] + ' @ ' + df['VTM'] + \
    ' ' + ' (' + df['gamepoints'] + ' pts)'
df['gamepoints'] = df['gamepoints'].astype(int)
df

df = df.sort_values('dates')

df['zone_count'] = df.groupby(['SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'PLAYER_ID'])['PLAYER_ID'].transform('count')


df