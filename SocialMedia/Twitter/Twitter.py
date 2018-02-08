import tweepy

from SocialMedia.SocialMedia import SocialMedia


def get_authorization_url(consumer_key, consumer_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    redirect_url = auth.get_authorization_url()
    return str(redirect_url)


def get_access_token_from_url(consumer_key, consumer_secret, response_url):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.get_authorization_url()

    from urllib import parse
    verifier = parse.parse_qs(parse.urlparse(response_url).query)['oauth_verifier'][0]
    print("Verifier:" + verifier)

    auth.get_access_token(verifier)
    print('Auth Token :' + str(auth.access_token))
    print('Auth Secret:' + str(auth.access_token_secret))

    return auth.access_token, auth.access_token_secret


class Twitter(SocialMedia):
    def __init__(self, client_id, client_secret, oauth_token, oauth_token_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        auth = tweepy.OAuthHandler(self.client_id, self.client_secret)
        auth.access_token = oauth_token
        auth.access_token_secret = oauth_token_secret
        self.twitter_api = tweepy.API(auth)

    def publish_update(self, message, ):
        self.twitter_api.update_status(status=message)

    def publish_update_with_attachment(self, body="", title="", url="",
                                       blog_name=""):
        pass

    def publish_update_with_image_attachment(self, message, image_path, url=""):
        self.twitter_api.update_with_media(filename=image_path, status=message)


if __name__ == '__main__':
    client_key = 'ecf8Ygwl3Sr9te5dvHoknoq7h'
    client_secret = 'xM7G3WocNnSYRCsIsJw7yeRDasuJ3QzxdRlS7iLZoVr92gKtAg'
    print(get_authorization_url(client_key, client_secret))
    access_token, access_token_secret \
        = get_access_token_from_url(client_key, client_secret, input("Response:"))

    twitter = Twitter(client_key,
                      client_secret,
                      access_token, access_token_secret)

    # Post Status working
    twitter.publish_update("Update with Text3!")

    # Post Image working
    twitter.publish_update_with_image_attachment("Update with Text and Image1", 'temp1.png')
