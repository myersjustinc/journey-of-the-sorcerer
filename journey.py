#!/usr/bin/env python
import json
import os
import sys

import requests


def get_rdio_access_token():
    r = requests.post(
        'https://services.rdio.com/oauth2/token',
        params={
            'grant_type': 'refresh_token',
            'refresh_token': os.environ['RDIO_REFRESH_TOKEN'],
        },
        auth=(os.environ['RDIO_CLIENT_ID'], os.environ['RDIO_CLIENT_SECRET'],))
    r.raise_for_status()
    return r.json()['access_token']


def get_rdio_playlists(access_token):
    r = requests.post(
        'https://services.rdio.com/api/1/getPlaylists',
        params={
            'method': 'getPlaylists',
            'extras': json.dumps([
                {'field': '*', 'exclude': 'true'},
                {'field': 'name'},
                {
                    'field': 'tracks',
                    'extras': [
                        {'field': '*', 'exclude': 'true'},
                        {'field': 'album'},
                        {'field': 'albumArtist'},
                        {'field': 'artist'},
                        {'field': 'duration'},
                        {'field': 'name'},
                        {'field': 'trackNum'},
                        {'field': 'isrcs'}
                    ]
                }
            ])
        },
        headers={'Authorization': 'Bearer {0}'.format(access_token)})
    r.raise_for_status()
    return r.json()['result']


def main(*args):
    pass


if __name__ == '__main__':
    main(*sys.argv[1:])
