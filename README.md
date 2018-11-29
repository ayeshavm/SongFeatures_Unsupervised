{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Pop and Country Songs Audio Features Analysis:\n",
    "\n",
    "### Background:\n",
    "\n",
    "The songs that we hear around these days, it is hard to distinguish a country song from a pop song, but is there really a difference between the two?  Are there song features which will be able to classify these two genres?\n",
    "\n",
    "\n",
    "\n",
    "<br>For this project, we will analyzing Pop and country songs from 1990 onwards using clustering analysis techniques.\n",
    "\n",
    "We will be extracting Spotify Features via the Spotify API, where the following data will be used:\n",
    "\n",
    "[Spotify Audio Features](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)\n",
    "- __acousticness__: describes how many acoustic sounds the track has vs. how many electric sounds [0.0 to 1.0] \n",
    "- __danceability__: describes how suitable a track is for dancing based on a combination of musical elements.\n",
    "  [0.0 least danceable to 1.0 most danceable)\n",
    "- duration_ms\n",
    "- __energy__: represents perceptual measure of intensity and activity.  typically energetic feels fast, loud and noisy.\n",
    "  [0.0 to 1.0]\n",
    "- instrumentalness\n",
    "- key\n",
    "- liveness\n",
    "- loudness\n",
    "- mode\n",
    "- speechiness\n",
    "- tempo\n",
    "- time signature\n",
    "- __valence__: measure from [0.0 to 1.0] describes the musical positiveness conveyed by a track.  Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)\n",
    "\n",
    "[Spotify Audio Analysis](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/)\n",
    "- bar length: a bar or measure is a segment of time as a given number of beats\n",
    "- beats length: The time interval of beats throughout the track.  A beat is the basic time unit of a piece of music.\n",
    "- sections length: defined by large ariation in rhythm or timbre e.g. chorus, verse, bridge, guitar solo etc.\n",
    "- segment length:  each segment contains a roughly consistent sound throughout its duration\n",
    "  * average & __median pitch__ - values from 0 to 1 that describe the relative dominance of every pitch in the scale.\n",
    "  * average & __median timbre__ - timbre is the quality of musical note or sound that distinguishes different types of \n",
    "    musical instruments or voices.\n",
    "\n",
    "\n",
    "We will be analyzing songs which have been tagged with the word 'pop' or 'country' from the Million Songs Database https://labrosa.ee.columbia.edu/millionsong/.\n",
    "\n",
    "and in the end specifically explore if there are differences between Taylor Swift's pre-pop - country songs and her pop songs.\n",
    "\n",
    "\n",
    "### Problem Definition:\n",
    "\n",
    "- How does country and pop music differ?  \n",
    "- Are there differences between the two music genres? -- Can we find some patterns that would differentiate these two music genres? \n",
    "- What patterns do we find with the song features?\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "\n",
    "\n",
    "### Limitations\n",
    "\n",
    "- since we are relying on the tags from the Million Songs Database to filter out pop and country songs, we can potentially have a 'noisy' data, since we could have jazz, rock songs, or songs with other genres which were added with incorrect tags.  But we should be able to see all these when we try to create clusters for our songs.  \n",
    "\n",
    "\n",
    "- Due to time constraints for this project, the analysis will just be done on Song Features from Spotify, and Lyrics analysis will be done as a future project.\n",
    "\n",
    "\n",
    " \n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Acquiring Data Set:\n",
    "\n",
    "Data sets were acquired from the different Sources:\n",
    "\n",
    "(1) To get the list of Artists, Songs, and genre tags records were extracted from the Million Song Database\n",
    "\n",
    " [Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. \n",
    "The Million Song Dataset. In Proceedings of the 12th International Society\n",
    "for Music Information Retrieval Conference (ISMIR 2011), 2011.](https://labrosa.ee.columbia.edu/millionsong/)\n",
    "\n",
    "<br>(2) To get audio features of the songs, Spotify API was used, given\n",
    "the artist name, and song title, the spotify Track ID can be retrieved, which can then be used to query the audio features for the song. [Code](https://github.com/ayeshavm/SongFeatures_Unsupervised/blob/master/source/getSpotifyAudioFeatures.py)\n",
    "\n",
    "\n",
    "(3) To get the lyrics of the songs, the Genius API will be used, to search the song based on a given Artist Name, and song title. [code](https://github.com/ayeshavm/SongFeatures_Unsupervised/blob/master/source/getGeniusLyrics.py).\n",
    "Code was adapted [from](https://github.com/johnwmillr/LyricsGenius)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "### Cleaning The Data and Feature Engineering:\n",
    "\n",
    "1) Combine the song data collected from Spotify with the Spotify Features, and the Lyrics collected from Genius.\n",
    "   Only keep records with both Spotify Features, and Lyrics Text from Genius.\n",
    "   \n",
    "   \n",
    "2) The Spotify Features extracted were in JSON format.  Reformatted records to create a column for every Spotify Feature attribute.\n",
    "\n",
    "3) Added a column 'genre' which was derived based on the tags found from the Song record.  A song was classified as 'pop' if 'pop' occurred in the tag the most, 'country' if 'country' occurred in the tag the most, otherwise, it will be tagged as 'other'.  This column will only be used for verifying output, but cannot provide a good score of accuracy since songs can be mis-tagged.  i.e. Beyonce's song records are tagged with 'country' instead of 'pop'.\n",
    "\n",
    "4) Lyrics Text were initially cleaned using nlp Language detector to remove tags, i.e. [Verses], [Chorus]. And used to filter out to only work with songs where Language == English.\n",
    "\n",
    "5)[Flesch-Kincaid Grade](https://en.wikipedia.org/wiki/Flesch–Kincaid_readability_tests) was derived from the Lyrics, but this feature did not show to be helpful in creating more distinct features, so was excluded in the final analysis.\n",
    "\n",
    "5) Additional data cleansing was done to filter out the noise from the mislabeled data from the Million Songs Database.  Genre tags were extracted from Spotify to update the genre labels of the songs, and filter out songs which are not labeled as country or pop.  The number of songs went down from 17001+ to 5881+.\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "collapsed": true
   },
   "source": [
    "### Analysis and results can be accessed [here](https://github.com/ayeshavm/SongFeatures_Unsupervised/blob/master/notebooks/00_SongsFeatureAnalysis_Unsupervised_Project.ipynb)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
