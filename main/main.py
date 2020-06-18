import argparse
from finder import GeniusAPI
from db.db import Mongo
from frequency import ArtistFrequency


def main(args):
    db = Mongo('lyrics-db')
    songs_in_db = db.getArtistCount(args.artist_name)
    if songs_in_db > 0:
        print('Artist found')
        x = ArtistFrequency(
            args.artist_name, db.getSongFrequency(args.artist_name)).getArtistLevelWordFrequency()

    else:
        print('Artist not Found in local database.\nSearching the world wide webs for {}\'s lyrics....\n'.format(
            args.artist_name))
        x = GeniusAPI(args.artist_name)
        x.get_lyrics()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get a list of all the words and their frequency an Artist has sang')
    parser.add_argument('-a', '--artist_name', dest='artist_name', type=str,
                        help='Specify the name of the artist you are searching for', required=True)
    args = parser.parse_args()
    main(args)
