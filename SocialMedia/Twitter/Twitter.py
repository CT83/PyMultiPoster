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
        self.post_id = None

    def publish_update(self, message, **kwargs):
        status = self.twitter_api.update_status(status=message)
        self.post_id = status.id_str

    def publish_update_with_image_attachment(self, message, image_url, url=""):
        status = self.twitter_api.update_with_media(filename=image_url, status=message)
        self.post_id = status.id_str

    def get_link_latest_post(self, post_id=None):
        try:
            if post_id is None:
                post_id = str(self.post_id)
                me = self.twitter_api.me()
                print(me)
                post_url = 'https://twitter.com/' + me.id_str + '/status/' + post_id
                return post_url
        except (TypeError, KeyError) as e:
            print(e)
            return ""

    def get_profile_name(self):
        profile = self.twitter_api.me()
        # print("Twitter get_profile:", profile.name)
        return profile.name


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
