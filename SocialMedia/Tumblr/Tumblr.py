from __future__ import print_function

from future import standard_library

from CONSTANT import TUMBLR_CLIENT_SECRET, TUMBLR_CLIENT_ID, TUMBLR_REDIRECT_URL
from SocialMedia.SocialMedia import SocialMedia
from SocialMedia.Tumblr.TumblrAuth import get_authorization_url, get_access_token_from_url

standard_library.install_aliases()
import pytumblr


# HTML and MD are supported by Tumblr

class Tumblr(SocialMedia):
    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    # TODO Make all extra function parameters same
    def __init__(self, client_id, client_secret, oauth_token, oauth_token_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        self.post_id = None
        self.blog_name = None

        self.tumblr_api = pytumblr.TumblrRestClient(
            self.client_id,
            self.client_secret,
            self.oauth_token,
            self.oauth_token_secret
        )

    def publish_update(self, message, blog_name="", title=""):
        self.post_id = self.tumblr_api.create_text(blog_name,
                                                   state="published",
                                                   slug="testing-text-posts",
                                                   title=title,
                                                   body=message)
        self.blog_name = blog_name

        print("Tumblr Post ID:", self.post_id)
        post_url = self.get_link_latest_post()
        print('Tumblr Post URL:', post_url)

    def publish_update_with_attachment(self, body="", title="", url="", blog_name=""):
        self.post_id = self.tumblr_api.create_link(blog_name, title=title, url=url,
                                                   description=body)
        self.blog_name = blog_name

        print("Tumblr Post ID:", self.post_id)

        post_url = self.get_link_latest_post()
        print('Tumblr Post URL:', post_url)

    def publish_update_with_image_attachment(self, caption="", image_links=None,
                                             tags=None, blog_name="",
                                             format="markdown",
                                             state="published"):
        # https://github.com/tumblr/pytumblr#creating-a-photo-post
        # image_links here is a list of all the images to be posted
        self.blog_name = blog_name

        if tags is None:
            tags = [""]
        self.post_id = self.tumblr_api.create_photo(blog_name,
                                                    state=state, tags=tags, format=format,
                                                    data=image_links,
                                                    caption=caption)
        print("Tumblr Post ID:", self.post_id)

        post_url = self.get_link_latest_post()
        print('Tumblr Post URL:', post_url)

    def get_link_latest_post(self, post_id=None):
        try:
            if post_id is None:
                post_id = str(self.post_id['id'])
                post_url = 'https://' + self.blog_name + '.tumblr.com/post/' + post_id
                return post_url
        except (TypeError, KeyError) as e:
            print(e)
            return ""


if __name__ == '__main__':
    url, res_key, res_sec = get_authorization_url(TUMBLR_CLIENT_ID,
                                                  TUMBLR_CLIENT_SECRET,
                                                  TUMBLR_REDIRECT_URL)
    print(url)
    tokens = get_access_token_from_url(TUMBLR_CLIENT_ID, TUMBLR_CLIENT_SECRET,
                                       res_key, res_sec,
                                       input('Allow then paste the full redirect URL here:\n'),
                                       callback_url=TUMBLR_REDIRECT_URL)
    tumblr = Tumblr(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret'],
    )

    # Post Status working
    tumblr.publish_update(
        message="""###Body Title""",
        title="Tit1le",
        blog_name='pymultiposter1')

    # Post Image working
    tumblr.publish_update_with_image_attachment(
        caption="""###Body Title""",
        image_links=["temp1.png", "temp3.png"],
        blog_name='pymultiposter1')

    # Post Link
    tumblr.publish_update_with_attachment(body="""###Body Title""",
                                          title="#Tile",
                                          url="www.googlel.com",
                                          blog_name="pymultiposter1")
