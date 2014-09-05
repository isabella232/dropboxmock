# #!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from urlparse import urlparse, parse_qs

from dropmock.core.utils import build_formatted_response
from dropmock.core.decorators import authenticate_oauth2
from dropmock.session import dbx_session_backend

#TODO in next release of this package: 
# manage document flow for different account


class ClientResponse(object):

    def __init__(self, backend):
        self.backend = backend


def token_from_oauth1(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/oauth2/token_from_oauth1
    global dbx_session_backend
    if not dbx_session_backend.is_connected(token='ABCDEFG'):
        dbx_session_backend.connect(token='ABCDEFG')
    return build_formatted_response(body={'access_token': 'ABCDEFG', 
                                          'token_type': 'bearer'},
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

def disable_access_token(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/disable_access_token
    global dbx_session_backend
    token = headers.get('access_token', '')
    oauth_token, oauth_token_secret = '', ''
    if token == '':
        oauth_token, oauth_token_secret = get_oauth_from_url(url)
        if ((oauth_token == '') and (request.parsed_body not in ['', None])):
            oauth_token = request.parsed_body.get('oauth_token', '')
    dbx_session_backend.disconnect(token=token, 
                                   oauth_token=oauth_token,
                                   oauth_token_secret=oauth_token_secret)
    return build_formatted_response(body={},
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

def get_oauth_from_url(url):
    parsed_url = urlparse(url, allow_fragments=True)
    query_string = parse_qs(parsed_url.query)
    oauth_token = query_string.get('oauth_token', '')
    oauth_token_secret = query_string.get('oauth_token_sercet', '')
    return oauth_token, oauth_token_secret

def account_info(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/account/info
    #TODO: retrieve different account info depending by request token
    return build_formatted_response(body={
            'referral_link': 'https://www.dropbox.com/referrals/r1a2n3d4m5s6t7',
            'display_name': 'John Doe',
            'uid': 12345678,
            'team': {
                'name': 'Elastic Inc.'
                },
            'country': 'IT',
            'quota_info': {
                'shared': 253738410565,
                'quota': 107374182400000,
                'normal': 680031877871
                }
            },
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)


def get_token(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/oauth2/token
    global dbx_session_backend
    if not dbx_session_backend.is_connected(token='ABCDEFG'):
        dbx_session_backend.connect(token='ABCDEFG')
    return build_formatted_response(body={'access_token': 'ABCDEFG', 
                                          'token_type': 'bearer', 
                                          'uid': '12345'},
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

def _build_metadata(list_metadata):
    # base metadata content
    _metadata = {
        'size': '225.4KB',
        'rev': '35e97029684fe',
        'thumb_exists': False,
        'bytes': 230783,
        'modified': 'Tue, 19 Jul 2011 21:55:38 +0000',
        'client_mtime': 'Mon, 18 Jul 2011 18:04:35 +0000',
        'path': '/Getting_Started.pdf',
        'is_dir': False,
        'icon': 'page_white_acrobat',
        'root': 'dropbox',
        'mime_type': 'application/pdf',
        'revision': 220823
        }
    if list_metadata:
        _metadata['contents'] = {
            'size': "2.3 MB",
            'rev': "38af1b183490",
            'thumb_exists': True,
            'bytes': 2453963,
            'modified': 'Mon, 07 Apr 2014 23:13:16 +0000',
            'client_mtime': 'Thu, 29 Aug 2013 01:12:02 +0000',
            'path': '/Photos/flower.jpg',
            'photo_info': {
              'lat_long': [
                37.77256666666666,
                -122.45934166666667
              ],
              'time_taken': 'Wed, 28 Aug 2013 18:12:02 +0000'
            },
            'is_dir': False,
            'icon': 'page_white_picture',
            'root': 'dropbox',
            'mime_type': 'image/jpeg',
            'revision': 14511
        }
    return _metadata


@authenticate_oauth2
def get_delta(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/delta
    cursor = request.parsed_body.get('cursor', [''])
    list_metadata = request.parsed_body.get('list', [False])
    if cursor[0] == '1st':
        body = {'entries':[['/photo', _build_metadata(list_metadata)],],
                'reset': False,
                'cursor': '2nd',
                'has_more': False}
    else:
        body = {'entries': [['/photo', _build_metadata(list_metadata)],],
                'reset': False,
                'cursor': '1st',
                'has_more': True}
    return build_formatted_response(body=body,
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

@authenticate_oauth2
def sandbox(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/metadata/sandbox
    # sandbox only retrieve 200 status code
    return build_formatted_response()

@authenticate_oauth2
def get_media(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/media/auto/
    body = {'url': 
            'https://dl.dropboxusercontent.com/1/view/abcdefghijk/example',
            'expires': (datetime.datetime.now()+datetime\
                .timedelta(hours=2)).isoformat(' ')}
    return build_formatted_response(body=body,
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

@authenticate_oauth2
def put_file(request, url, headers, *args, **kwargs):
    # mock https://api-content.dropbox.com/(\d+)/files_put/([a-zA-Z]+)/([a-zA-Z]+)
    global dbx_session_backend
    #TODO: get document file path (not only name) from url
    # and manage it in a session backend dictionary
    return build_formatted_response(body=body,
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)
