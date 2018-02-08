import tweepy

from SocialMedia.SocialMedia import SocialMedia


def get_access_tokens(consumer_key, consumer_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    try:
        redirect_url = auth.get_authorization_url()
        print("Redirect URL", str(redirect_url))
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
    token = auth.request_token
    verifier = input('Verifier:')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.request_token = token
    try:
        auth.get_access_token(verifier)
        print('Got access!!')
        print('Auth' + str(auth))
        print('Auth Token:' + auth.access_token)
        print('Auth Secret:' + auth.access_token_secret)
        return auth.access_token, auth.access_token_secret
        # api = tweepy.API(auth)
        # api.update_status(status="Sent fomre ")
    except tweepy.TweepError:
        print('Error! Failed to get access token.')


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
    # access_token, access_token_secret \
    #     = get_authorization_url(client_key,
    #                         client_secret)
    access_token = "957098797791768576-iBgwacSqxbsFM3cah3fndBjndLm8eOO"
    access_token_secret = "7VNkIwputPvlhWhBnltCJu9Ct9INAN5vOfgtls00YtF8x"
    twitter = Twitter(client_key,
                      client_secret,
                      access_token, access_token_secret)

    # Post Status working
    # twitter.publish_update("Update with Text3!")

    # Post Image working
    # twitter.publish_update_with_image_attachment("Update with Text and Image1", 'temp1.png')
