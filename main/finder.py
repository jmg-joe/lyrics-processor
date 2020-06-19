import requests
import os
import argparse
import re
from frequency import FrequencyCreator, ArtistFrequency
from db.db import *
from bs4 import BeautifulSoup as bs

defaults = {
    'api_token': os.environ.get("GENIUS_API_KEY"),
    'root_api_url': os.environ.get("GENIUS_ROOT_API_URL")
}


class GeniusAPI:
    def __init__(self, artist):
        self._endpoint = defaults['root_api_url'] + '/search'
        self._headers = {'Authorization': 'Bearer ' +
                                          defaults['api_token']}
        self._artist = artist

    def get_lyrics(self):
        page = 1
        while page < 8:
            data = {'q': self._artist, 'page': page}
            api_response = requests.get(self._endpoint, data=data, headers=self._headers).json()
            for potential_song in api_response['response']['hits']:
                if self._artist.lower() in potential_song['result']['primary_artist']['name'].lower():
                    song_found = potential_song
                    song_url = song_found['result']['url']
                    try:
                        lyrics_to_save = self.scrape_lyrics(song_url)
                        self.write_to_dir(lyrics_to_save,
                                      song_found['result']['title'], self._artist)
                    except:
                        print('could not process lyrics for ' + song_found['result']['title'] + ' with url ' + song_url)
                        continue

            page += 1
        print('All Songs for {} have been found. Program is now calculating the frequency of all words...'.format(
            self._artist))
        db = Mongo('lyrics-db')
        songs_in_db = db.getSongArtistCount(self._artist)
        if songs_in_db > 0:
            artistFreq = ArtistFrequency(self._artist, db.getSongFrequency(self._artist))
            artistFreq.createArtistLevelWordFrequency()

    def scrape_lyrics(self, url):
        web_page = requests.get(url)
        html = bs(web_page.text, 'html.parser')
        [h.extract() for h in html('script')]
        lyrics = html.find('div', class_='lyrics').get_text()
        return lyrics

    def write_to_dir(self, lyrics, song, artist):
        # remove special characters from artist and song
        artist = artist.replace('/', '')
        song = re.sub('[^a-zA-Z0-9 \n\.]', '', song)

        if os.path.isdir('../lyrics_dir/{}'.format(artist)):
            path_name = '../lyrics_dir/{}/{}.txt'.format(artist, song)
            self.write_txt_file(lyrics, song, artist, path_name)
            fc = FrequencyCreator(path_name)
            frequency = fc.process_lyrics()
            song_frequency = {'artist': artist, 'song': song, 'lyrics_freq': frequency}
            db = Mongo('lyrics-db')
            db.saveSongFrequency(song_frequency)
        else:
            os.makedirs('../lyrics_dir/{}'.format(artist))
            path_name = '../lyrics_dir/{}/{}-{}.txt'.format(artist, song, artist)
            self.write_txt_file(lyrics, song, artist, path_name)

    def write_txt_file(self, lyrics, song, artist, path):
        f = open(path, 'w')
        f.write('Song: {}'.format(song) + '\n')
        f.write('Artist: {}'.format(artist) + '\n')
        f.write(lyrics)
        f.close()
