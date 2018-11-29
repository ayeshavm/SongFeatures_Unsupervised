#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 10:41:30 2018
This program will retrieve Spotify ID/URI given an ArtistID and Song Title
And will retrieve the Audio Track features, and Audio Analysis features using the Spotify URI
@author: ayeshamendoza
"""
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


client_id = SpotifyClientID
client_secret = SpotifyClientSecret

##Query artist to get track IDs

def get_Spotify_trackID(title, artist):
    ''' this function send query request to Spotify by title and artist name
        and will return corresponding the track ID'''
    
    urilist = []
    error = 0
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=False
    search_query = title + ' ' + artist
    
    try:
        result = sp.search(search_query)
        #find a song that matches the title and artist from the query result
        for i in result['tracks']['items']:
            if (i['artists'][0]['name'] == artist) and (i['name'] == title):
                urilist.append(i['uri'])
                return (urilist, error)
                break

    except:
        error = 999
        print('get_Spotify_trackID error processing : ', title, artist)
    
    
                
    return (urilist, error)
    
### Getting audio data:

def getFeatures(uri):
    '''this function will send query request to Spotify for audio features for the specified uri'''
    
    features = []
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    error = 0
    try:
        features = sp.audio_features(uri)
    except:
        error = 888
        print('getFeatures error processing : ' ,uri)
    
    return (features, error)

def getAudioAnalysis(uri):
    '''this function will send query request to Spotify for audio analysis for the specified uri'''
    
    features = []
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    error = 0
    try:
        features = sp.audio_analysis(uri)
    except:
        error = 888
        print('getFeatures error processing : ' ,uri)
    
    return (features, error)

def processAudioDict(audioAnalysis):
    '''This function will process the Audio Analysis Features and save into a dictionary format for
       pitch_mean, pitch_med, timbre_mean, timbre_med, bar length, beat length and segment length'''

    audioDict = {}
    

    sum_pitch_mean = 0
    sum_pitch_median = []
    song_pitch_mean = 0
    song_pitch_med = 0

    sum_timbre_mean = 0
    sum_timbre_median = []
    song_timbre_mean = 0
    song_timbre_med = 0

    seg_len = len(audioAnalysis['segments']) 
    
    audioDict['bar_len'] = len(audioAnalysis['bars'])
    audioDict['beat_len'] = len(audioAnalysis['beats'])
    audioDict['seg_len'] = seg_len
    
    for i in range(seg_len):
 
        pitches = np.array(audioAnalysis['segments'][i]['pitches'])
        timbre = np.array(audioAnalysis['segments'][i]['timbre'])
        mean_pitch = np.mean(pitches)
        med_pitch = np.median(pitches)
        sum_pitch_mean += mean_pitch
        sum_pitch_median.append(med_pitch)
    
        mean_timbre = np.mean(timbre)
        med_timbre = np.median(timbre)
        sum_timbre_mean += mean_timbre
        sum_timbre_median.append(med_timbre)
    
    song_pitch_mean = sum_pitch_mean / seg_len
    song_timbre_mean = sum_timbre_mean / seg_len
    song_pitch_med = np.median(np.array(sum_pitch_median))
    song_timbre_med = np.median(np.array(sum_timbre_median))

    audioDict['pitch_mean'] = song_pitch_mean
    audioDict['pitch_med'] = song_pitch_med
    audioDict['timbre_mean'] = song_timbre_mean
    audioDict['timbre_med'] = song_timbre_med
    
    return audioDict




songsDF = pd.read_pickle('../data/msongs/out/Songs_NLP_allFeatures_1b.p')

songsDF.drop_duplicates(subset=['artist_id', 'title'], inplace=True)

songsDF.reset_index(inplace=True)

x = 0
dflen = len(songsDF)

for i, row in enumerate(songsDF.itertuples(), start=0):
    
    # get track id:
    urilist, err = get_Spotify_trackID(row.title, row.artist_name)
    if err > 0:
        print('...breaking')
        songsDF.to_pickle('spotify_1118_bkp.p')
        #break
    else: 
        if len(urilist) == 1:
            #print('getting Features....')
            uri = urilist[0].split(':')[2]
            songFeatures, err = getFeatures(uri)
            if err > 0:
                print('breaking....')
                songsDF.to_pickle('spotify_1118_bkp.p')
                #break
            else:
                songsDF.set_value(i,'spotifyURI',uri)
                songsDF.set_value(i,'songFeatures',songFeatures)
                
                audioAnalysis, err = getAudioAnalysis(uri)
                if err > 0:
                    print('breaking....')
                    songsDF.to_pickle('spotify_1118_bkp.p')
                else:
                    audioDict = processAudioDict(audioAnalysis)
                    songsDF.set_value(i,'bar_len',audioDict['bar_len'])
                    songsDF.set_value(i,'beat_len',audioDict['beat_len'])
                    songsDF.set_value(i,'seg_len',audioDict['seg_len'])
                    songsDF.set_value(i,'pitch_mean',audioDict['pitch_mean'])
                    songsDF.set_value(i,'pitch_med',audioDict['pitch_med'])
                    songsDF.set_value(i,'timbre_mean',audioDict['timbre_mean'])
                    songsDF.set_value(i,'timbre_med',audioDict['timbre_med'])
                    
    if (x < dflen) & (x % 200 == 0):
        print('processing row {}'.format(i), row.title, row.artist_name)
        songsDF.to_pickle('spotify_1118_bkp.p')
    x += 1
    
print('Get Spotify Features for pop songs ended')
songsDF.to_pickle('SpotifyAudioFeatures_done.p')

print(songsDF[['artist_name','title','spotifyURI','songFeatures','bar_len','beat_len']][:10])

