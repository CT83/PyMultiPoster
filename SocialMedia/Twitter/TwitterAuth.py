def get_authorization_url_auth(consumer_key, consumer_secret, callback=None):
    from tweepy import OAuthHandler
    auth = OAuthHandler(consumer_key, consumer_secret, callback)
    redirect_url = auth.get_authorization_url()
    key = auth.request_token['oauth_token']
    secret = auth.request_token['oauth_token_secret']
    return redirect_url, key, secret


def get_access_token_from_url(response_url, consumer_key, consumer_secret, token):
    from urllib import parse
    verifier = parse.parse_qs(parse.urlparse(response_url).query)['oauth_verifier'][0]

    from tweepy import OAuthHandler
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.get_authorization_url()
    auth.request_token['oauth_token'] = token[0]
    auth.request_token['oauth_token_secret'] = token[1]
    auth.get_access_token(verifier)

    print('Twitter Auth Token :' + str(auth.access_token))
    print('Twitter Auth Secret:' + str(auth.access_token_secret))

    return auth.access_token, auth.access_token_secret
