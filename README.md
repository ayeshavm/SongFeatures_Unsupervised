

# Pop and Country Songs Audio Features Analysis:
Song Features Analysis of Country and Pop Songs from 1990s onwards Using Clustering Analysis Techniques


### Background:

The songs that we hear around these days, it is hard to distinguish a country song from a pop song, but is there really a difference between the two?  Are there song features which will be able to classify these two genres?



<br>For this project, __we will analyzing Pop and country songs from 1990 onwards__, and we will be extracting Spotify Features via the Spotify API, where the following data will be used:

[Spotify Audio Features](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)
- __acousticness__: describes how many acoustic sounds the track has vs. how many electric sounds [0.0 to 1.0] 
- __danceability__: describes how suitable a track is for dancing based on a combination of musical elements.
  [0.0 least danceable to 1.0 most danceable)
- duration_ms
- __energy__: represents perceptual measure of intensity and activity.  typically energetic feels fast, loud and noisy.
  [0.0 to 1.0]
- instrumentalness
- key
- liveness
- loudness
- mode
- speechiness
- tempo
- time signature
- __valence__: measure from [0.0 to 1.0] describes the musical positiveness conveyed by a track.  Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)

[Spotify Audio Analysis](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/)
- bar length: a bar or measure is a segment of time as a given number of beats
- beats length: The time interval of beats throughout the track.  A beat is the basic time unit of a piece of music.
- sections length: defined by large ariation in rhythm or timbre e.g. chorus, verse, bridge, guitar solo etc.
- segment length:  each segment contains a roughly consistent sound throughout its duration
  * average & __median pitch__ - values from 0 to 1 that describe the relative dominance of every pitch in the scale.
  * average & __median timbre__ - timbre is the quality of musical note or sound that distinguishes different types of 
    musical instruments or voices.

We will be analyzing songs which have been tagged with the word 'pop' or 'country' from the Million Songs Database https://labrosa.ee.columbia.edu/millionsong/.

and in the end specifically explore if there are differences between Taylor Swift's pre-pop - country songs and her pop songs.


### Problem Definition:

- How does country and pop music differ?  
- Are there differences between the two music genres? -- Can we find some patterns that would differentiate these two music genres? 
- What patterns do we find with the song features?


Full Analysis with Findings can be accessed in the main notebook: [00_SongFeaturesAnalysis_Unsupervised_Project.ipynb](https://github.com/ayeshavm/SongFeatures_Unsupervised/blob/master/notebooks/00_SongsFeatureAnalysis_Unsupervised_Project.ipynb)


