from datetime import timedelta
from pathlib import Path
import unittest
from xml.etree import ElementTree

from journey.reader.favorites import albums_songs


class AlbumsSongsBase(unittest.TestCase):
    def setUp(self):
        self.fixtures_path = Path(__file__).parent / 'fixtures'
        self.albums_songs_path = (
            self.fixtures_path / 'favorites_albumsandsongs.xspf')
        self.xspf = ElementTree.parse(str(self.albums_songs_path))


class TrackTestCase(AlbumsSongsBase):
    def setUp(self, *args, **kwargs):
        super(self.__class__, self).setUp(*args, **kwargs)

        self.raw_coins = self.xspf.find('.//{http://xspf.org/ns/0/}track[1]')
        self.coins = albums_songs.Track(self.raw_coins)

        self.raw_room = self.xspf.find('.//{http://xspf.org/ns/0/}track[2]')
        self.room = albums_songs.Track(self.raw_room)

    def test_title(self):
        self.assertEqual(
            self.coins.title, 'Coins In A Fountain',
            'Title improperly parsed')

    def test_creator_name(self):
        self.assertEqual(
            self.coins.creator_name, 'Passenger',
            'Creator name improperly parsed')

    def test_album_name(self):
        self.assertEqual(
            self.coins.album_name, 'Whispers (Deluxe)',
            'Album name improperly parsed')

    def test_track_number(self):
        self.assertEqual(
            self.coins.track_number, 1,
            'Track number improperly parsed')

    def test_duration_ms(self):
        self.assertEqual(
            self.coins.duration, timedelta(seconds=182),
            'Millisecond duration improperly parsed')

    def test_duration_us(self):
        self.assertEqual(
            self.room.duration, timedelta(seconds=318),
            'Microsecond duration improperly parsed')

    def test_isrcs(self):
        self.assertEqual(
            self.coins.isrcs, ('GBMQN1400001',),
            'ISRCs improperly parsed')


class AlbumsSongsExtractorTestCase(AlbumsSongsBase):
    def setUp(self, *args, **kwargs):
        super(self.__class__, self).setUp(*args, **kwargs)
        self.extractor = albums_songs.AlbumsSongsExtractor(
            self.albums_songs_path)

    def test_xspf_loaded(self):
        self.assertIsInstance(
            self.extractor.xspf, ElementTree.ElementTree,
            'XSPF not properly loaded')

    def test_tracks(self):
        self.assertEqual(
            len(self.extractor.tracks()), 6,
            'Not all tracks extracted')

    def test_parse_tracks(self):
        self.assertEqual(
            len(self.extractor._parse_tracks(self.xspf)), 6,
            'Not all tracks extracted')

    def test_first_track(self):
        self.assertEqual(
            self.extractor.tracks()[0].title, 'Coins In A Fountain',
            'First track improperly parsed')
