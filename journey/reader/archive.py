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
