from __future__ import print_function

from future import standard_library

from SocialMedia.SocialMedia import SocialMedia

standard_library.install_aliases()
import pytumblr
from requests_oauthlib import OAuth1Session


def get_access_tokens(consumer_key, consumer_secret):
    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    # STEP 1: Obtain request token
    oauth_session = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth_session.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    # STEP 2: Authorize URL + Rresponse
    full_authorize_url = oauth_session.authorization_url(authorize_url)

    # Redirect to authentication page
    print('\nPlease go here and authorize:\n{}'.format(full_authorize_url))
    redirect_response = input('Allow then paste the full redirect URL here:\n')

    # Retrieve oauth verifier
    oauth_response = oauth_session.parse_authorization_response(redirect_response)

    verifier = oauth_response.get('oauth_verifier')

    # STEP 3: Request final access token
    oauth_session = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier
    )
    oauth_tokens = oauth_session.fetch_access_token(access_token_url)

    tokens = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': oauth_tokens.get('oauth_token'),
        'oauth_token_secret': oauth_tokens.get('oauth_token_secret')
    }

    return tokens


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
        if image_links is None:
            image_links = [""]
        self.tumblr_api.create_photo(blog_name,
                                     state=state, tags=tags, format=format,
                                     data=image_links,
                                     caption=caption)


if __name__ == '__main__':
    tokens = get_access_tokens("h8QTvJw4B8xMDo9GAFXC8Ll7xbX99MUhDiIA7AFBIfH2cuNzy3",
                               "g8Kgg8fIm8W8YadqqJy5mKR0dzUGYQXYwg1GvNHLofpgmohQoe")
    print(tokens)
    tumblr = Tumblr(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret'],
    )

    # Post Status working
    # tumblr.publish_update(
    #     body="""###Body Title""",
    #     title="Tit1le",
    #     blog_name='pymultiposter1')

    # Post Image working
    # tumblr.publish_update_with_image_attachment(
    #     caption="""###Body Title""",
    #     image_links=["temp1.png", "temp3.png"],
    #     blog_name='pymultiposter1')

    # Post Link
    # tumblr.publish_update_with_attachment(body="""###Body Title""",
    #                                       title="#Tile",
    #                                       url="www.googlel.com",
    #                                       blog_name="pymultiposter1")