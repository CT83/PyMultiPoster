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
    # TODO Add format to all functions
    def __init__(self, client_id, client_secret, oauth_token, oauth_token_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        self.tumblr_api = pytumblr.TumblrRestClient(
            self.client_id,
            self.client_secret,
            self.oauth_token,
            self.oauth_token_secret
        )

    def publish_update(self, body, title="", blog_name="", state="published",
                       slug="testing-text-posts"):
        print(self.tumblr_api.create_text(blog_name,
                                          state=state,
                                          slug=slug,
                                          title=title,
                                          body=body))

    def publish_update_with_attachment(self, body="", title="", url="",
                                       blog_name=""):
        self.tumblr_api.create_link(blog_name, title=title, url=url, description=body)

    def publish_update_with_image_attachment(self, caption="", image_links=None,
                                             tags=None, blog_name="",
                                             format="markdown",
                                             state="published"):
        # https://github.com/tumblr/pytumblr#creating-a-photo-post
        if tags is None:
            tags = [""]
        print("Tumblr Posting Update with Image:", image_links)
        self.tumblr_api.create_photo(blog_name,
                                     state=state, tags=tags, format=format,
                                     data=image_links,
                                     caption=caption)


if __name__ == '__main__':
    # TODO This needs to be tested
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
        body="""###Body Title""",
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
