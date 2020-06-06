# Flying Saucers
# Softdev2 pd9
# P05 -- The Bookshelf / Google API Calls
# 2020-06-05

import http.client
import json
from urllib.parse import urlencode
import os

# early prep for future apache deployment
DIR = os.path.dirname(__file__) or '.'
DIR += '/'

# =============== TOKEN RETRIEVAL ===============

def gen_authlink(callback):
    """Generate link for user to authorize account access."""
    scopes = ['https://www.googleapis.com/auth/drive.file']
    params = {
        'client_id':CLIENT_ID,
        'redirect_uri':callback,
        'response_type':'code',
        'scope':' '.join(scopes),
        'access_type':'offline', # i don't fully understand this one tbh
        # should i add state? idk
        'prompt':'consent'
        }
    return 'https://accounts.google.com/o/oauth2/v2/auth?'+urlencode(params)
    pass

def trade_for_tokens(authcode,redirect_uri):
    """Requests access/refresh tokens using the callback authorization code.

    See: https://developers.google.com/identity/protocols/oauth2/web-server,  HTTP/REST Step 5

    """
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    body = urlencode({
        'code':authcode,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET,
        'redirect_uri':redirect_uri,
        'grant_type':'authorization_code'
        })
    conn = http.client.HTTPSConnection('oauth2.googleapis.com')
    conn.request('POST','/token',headers=headers,body=body)
    response = conn.getresponse()
    print(response)
    print(response.read())
    pass

def replace_access_tokens(refresh_token):
    """For when access token expires, get new access token"""
    pass

# =============== GOOGLE DOCS ===============


# =============== INITIALIZATIONS ===============

with open(DIR+'../keys.json','r') as keyfile:
    keys = json.loads(keyfile.read())
    CLIENT_ID = keys['google_client_id']
    CLIENT_SECRET = keys['google_client_secret']

# =============== TEST CODE ===============

# print(gen_authlink('http://localhost:5000/google_oauth'))
