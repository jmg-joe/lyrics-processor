import operator
import argparse
import re
from db.db import *


class FrequencyCreator:
    def __init__(self, song):
        self._song = song

    def stripSongOnlyLyrics(self):
        with open(self._song, 'r') as f:
            lines = f.readlines()
        with open('temp.txt', 'w') as f:
            i = 0
            for line in lines:
                if (('[' and ']') not in line.strip('\n')) and ('Song:' not in line.strip('\n')) and (
                        'Artist:' not in line.strip('\n')):
                    f.write(line)
                i += 1

    def process_lyrics(self):
        self.stripSongOnlyLyrics()
        document_text = open('temp.txt', 'r')
        text_string = document_text.read().lower()
        match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
        frequencyDict = self.createWordFrequencyDict(match_pattern)
        return frequencyDict

    def createWordFrequencyDict(self, words):
        frequency = {}
        for word in words:
            count = frequency.get(word, 0)
            frequency[word] = count + 1
        return frequency


class ArtistFrequency:
    def __init__(self, artist, frequency):
        self._artist = artist
        self._frequency = frequency

    def createArtistLevelWordFrequency(self):
        all_artists_lyric_frequency = {}
        all_songs_lyrics = self._frequency
        for song in all_songs_lyrics:
            song_freq = song['lyrics_freq']
            for word, freq in song_freq.items():
                count = all_artists_lyric_frequency.get(word, freq)
                try:
                    all_artists_lyric_frequency[word] = count + freq
                except KeyError:
                    all_artists_lyric_frequency[word] = freq
        sorted_artist_word_frequency = dict(sorted(all_artists_lyric_frequency.items(),
                                                   key=operator.itemgetter(1)))
        db = Mongo('lyrics-db')
        db.saveDiscographyFrequency({'artist': self._artist, 'all_lyrics': sorted_artist_word_frequency})
        print('Frequency for {} has been calculated...'.format(self._artist))

    def getArtistLevelWordFrequency(self):
        db = Mongo('lyrics-db')
        return db.getDiscographyFrequency(self._artist)
