from __future__ import print_function

from future import standard_library

standard_library.install_aliases()

from requests_oauthlib import OAuth1Session


def get_authorization_url(consumer_key, consumer_secret, callback_url=""):
    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    oauth_session = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret,
                                  callback_uri=callback_url)
    fetch_response = oauth_session.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    full_authorize_url = oauth_session.authorization_url(authorize_url)

    return full_authorize_url, resource_owner_key, resource_owner_secret


def get_access_token_from_url(consumer_key, consumer_secret,
                              resource_owner_key, resource_owner_secret,
                              redirect_response, callback_url=None):
    access_token_url = 'http://www.tumblr.com/oauth/access_token'
    oauth_session = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                  callback_uri=callback_url)

    oauth_response = oauth_session.parse_authorization_response(redirect_response)
    verifier = oauth_response.get('oauth_verifier')
    oauth_session = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
        callback_uri=callback_url
    )
    oauth_tokens = oauth_session.fetch_access_token(access_token_url)

    token = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': oauth_tokens.get('oauth_token'),
        'oauth_token_secret': oauth_tokens.get('oauth_token_secret')
    }

    return token
