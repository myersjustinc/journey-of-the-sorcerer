from zipfile import ZipFile

from journey.reader.xspf import XSPF


class Archive(object):
    """
    Expose information from all relevant files in an Rdio farewell dump.

    Positional arguments:
    archive_path -- A path (pathlib.Path or str) to an Rdio export ZIP file.
    """
    def __init__(self, archive_path):
        self._zip = ZipFile(str(archive_path), 'r')

    def favorites(self):
        """Parse the user's list of favorited songs."""
        return XSPF(
            self._zip.open('1_favorites/favorites_albumsandsongs.xspf'))

    def playlists(self):
        """Parse the user's created playlists."""
        all_files = self._zip.infolist()
        created_playlists = filter(
            lambda file_info: (
                file_info.filename.startswith('3_playlists/created/') and
                file_info.filename.endswith('.xspf')),
            all_files)
        return tuple([
            XSPF(self._zip.open(file_info))
            for file_info in created_playlists])
