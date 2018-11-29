#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 10:41:30 2018
This program will retrieve lyrics from Genius.com
@author: ayeshamendoza
"""
import pandas as pd
import lyricsgenius as genius

def getGeniusLyrics(title, artist_name):
    
    lyrics = ''
    err = 0
    api = genius.Genius(GeniusAccessToken)
    try:
        song = api.search_song(title, artist_name)
        lyrics = song.lyrics
    except:
        err = 999
        print('error searching for song {}, {}'.format(title, artist_name))
        
    return lyrics, err

#countrySongs = pd.read_pickle('../data/msongs/out/countrySongs.p')
#popSongs = pd.read_pickle('../data/msongs/out/countrySongs.p')

popSongs = pd.read_pickle('DFPopSongs.p')

pop = popSongs[((popSongs.year >= 1990) & (popSongs.year < 1995)) | (popSongs.year > 2000)].copy().reset_index()

api = genius.Genius(GeniusAccessToken)

record_count = 0

#for restart
#- update indices, and start index in FOR loop
#- update filenames

#for i, row in enumerate(pop[0:11].itertuples(), start=0):
for i, row in enumerate(pop[60000:80000].itertuples(), start=60000):
    
    # get track id:
    lyrics, err = getGeniusLyrics(row.title, row.artist_name)
    
    
    if err > 0:
        print('...breaking')
        #break
    else: 
        if len(lyrics) > 0:
            pop.set_value(i,'lyrics_text',lyrics)
            
    record_count += 1
    if (record_count < len(pop)) and (record_count % 1000 == 0):
        pop.to_pickle('DFpop_bkp_1110.p')
        print(row.title, row.artist_name)
        print('saving to file record_count {}'.format(record_count))
    
print('program ended successfully, processed {} records'.format(record_count))        
pop.to_pickle('DFPopLyrics_111018_60to80000.p')
    