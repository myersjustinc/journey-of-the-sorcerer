from datetime import timedelta
from xml.etree import ElementTree


xspf_ns = {'xspf': 'http://xspf.org/ns/0/'}


class Track(object):
    """
    Parse and manage information for a single track.

    Positional arguments:
    track_elem   -- An ElementTree.Element representing a <track> element from
                    an XSPF document.
    """
    def __init__(self, track_elem):
        self.track_elem = track_elem
        self._parse()

    def _parse(self):
        """Parse all properties of the given track."""
        self.title = self._extract_title()
        self.creator_name = self._extract_creator_name()
        self.album_name = self._extract_album_name()
        self.track_number = self._extract_track_number()
        self.duration = self._extract_duration()
        self.isrcs = self._extract_isrcs()

    def _get_child(self, tag_name):
        """Return a child XSPF tag of the given name."""
        return self.track_elem.find('./xspf:{0}'.format(tag_name), xspf_ns)

    def _extract_title(self):
        """Extract the title of the track."""
        return self._get_child('title').text

    def _extract_creator_name(self):
        """Extract the name of the track's creator (i.e., artist)."""
        return self._get_child('creator').text

    def _extract_album_name(self):
        """Extract the name of the track's album."""
        return self._get_child('album').text

    def _extract_track_number(self):
        """Extract the number of the track's position on its album."""
        return int(self._get_child('trackNum').text)

    def _extract_duration(self):
        """Extract the length of the track."""
        raw_duration = int(self._get_child('duration').text)
        if raw_duration < 1e6:
            return timedelta(milliseconds=raw_duration)
        return timedelta(microseconds=raw_duration)

    def _extract_isrcs(self):
        """Extract the ISRCs (recording IDs) of the track."""
        isrc_elems = self.track_elem.findall(
            './xspf:meta[@rel="https://rdio.com/xspf/t/isrcs"]', xspf_ns)
        return tuple([isrc_elem.text for isrc_elem in isrc_elems])


class XSPF(object):
    """
    Expose album/song information from a given Rdio XSPF export file.

    Positional arguments:
    xspf_path    -- A path (pathlib.Path or str) to a XSPF file to load.
    """
    def __init__(self, xspf_path):
        self._doc = ElementTree.parse(str(xspf_path))

    def tracks(self):
        """Extract track information from our XSPF file."""
        return self._parse_tracks(self._doc)

    def _parse_tracks(self, doc):
        """
        Return a dict for each track in the given XSPF file.

        Positional arguments:
        doc  -- An ElementTree representing an XSPF document.
        """
        raw_tracks = doc.findall('./xspf:trackList/xspf:track', xspf_ns)
        return [Track(raw_track) for raw_track in raw_tracks]
