#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 10:41:30 2018
This program will retrieve genre labels in Spotify Artist and derive final label based on number of occurrences
of 'pop', 'country' or other in the label.  The genre label is a list, so it can have more than one label.
@author: ayeshamendoza
"""
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = SpotifyClientID
client_secret = SpotifyClientSecret

##Query artist to get track IDs

def get_Spotify_trackID(title, artist):
    ''' this function send query request to Spotify by title and artist name
        and will return corresponding the track ID'''
    
    artistid = ''
    error = 0
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=False
    search_query = title + ' ' + artist
    
    try:
        result = sp.search(search_query)
        #find a song that matches the title and artist from the query result
        for i in result['tracks']['items']:
            if (i['artists'][0]['name'] == artist):
                artistid = i['artists'][0]['id']
                return (artistid, error)
                break
    except:
        error = 999
        print('get_Spotify_trackID error processing : ', title, artist)
    
    
                
    return (artistid, error)
    
### Getting audio data:


def getArtist(artistid):
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=False
    err = 0
    genres = []

    try:
        result = sp.artist(artistid)
        genres = result['genres']
        #print(genres)
    except:
        print('error')
        err = 555
        
    return (genres, err)


import pandas as pd
songsDF = pd.read_pickle('../data/msongs/out/SongsSpotifyFeaturesAll.p')

songsDF.drop_duplicates(subset=['artist_id', 'artist_name'], inplace=True)

songsDF.reset_index(inplace=True,drop=True)

artistDF = songsDF[['artist_id','artist_name','title']].copy()
x = 0


for i, row in enumerate(artistDF.itertuples(), start=0):
    
    # get artist id:
    artistid, err = get_Spotify_trackID(row.title, row.artist_name)
    if err > 0:
        print('...breaking')
        artistDF.to_pickle('spotifyGenre_1122_bkp.p')
        #break
    else: 
        if artistid != '':
            genre, err = getArtist(artistid)
            if err > 0:
                print('breaking....')
                artistDF.to_pickle('spotifyGenre_1122_bkp.p')
                #break
            else:
                genre_count = {'country': 0, 'pop': 0, 'other':0}
                
                for tag in genre:
                    str1 = tag.strip().lower()
                    
                    if (str1.find('pop')) != -1:  #string contains pop
                        genre_count['pop'] += 1
                    elif (str1.find('country')) != -1:  #string contains country
                        genre_count['country'] += 1
                    else:
                        genre_count['other'] += 1                    
                    
                artistDF.set_value(i,'SpotifyGenre', max(genre_count, key=lambda key: genre_count[key]))
                artistDF.set_value(i,'country_count', genre_count['country'])
                artistDF.set_value(i,'pop_count', genre_count['pop'])
                artistDF.set_value(i,'other_count', genre_count['other'])                  

                artistDF.set_value(i,'spotifyArtistID',artistid)

                        
    if (x % 100 == 0):
        print('processing row {}'.format(i), row.title, row.artist_name)
        artistDF.to_pickle('spotifyGenre_1122_bkp.p')
    x += 1
    
print('Get Spotify Features for pop songs ended')
artistDF.to_pickle('SpotifyArtistGenre_done.p')

print(artistDF.head())



