import tweepy

from CONSTANT import TWITTER_CLIENT_SECRET, TWITTER_CLIENT_ID
from SocialMedia.SocialMedia import SocialMedia


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
    client_key = TWITTER_CLIENT_ID
    client_secret = TWITTER_CLIENT_SECRET
    # TODO Fix This
    twitter_auth = TwitterAuth(TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET)
    url, oauth = twitter_auth.get_authorization_url()
    print(url)
    access_token, access_token_secret \
        = twitter_auth.get_access_token_from_url(input("Response:"))

    twitter = Twitter(client_key,
                      client_secret,
                      access_token, access_token_secret)

    # Post Status working
    twitter.publish_update("Update with Text3!")

    # Post Image working
    twitter.publish_update_with_image_attachment("Update with Text and Image1", 'temp1.png')
