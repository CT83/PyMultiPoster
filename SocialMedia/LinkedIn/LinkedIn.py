from linkedin.linkedin import LinkedInApplication, LinkedInAuthentication

from CONSTANT import LINKEDIN_CLIENT_SECRET, LINKEDIN_CLIENT_ID, LINKEDIN_RETURN_URL
from SocialMedia.SocialMedia import SocialMedia


def get_authorization_url(consumer_key, consumer_secret, return_url=LINKEDIN_RETURN_URL):
    linkedin_auth = LinkedInAuthentication(
        consumer_key,
        consumer_secret,
        return_url,
        permissions=['r_basicprofile',
                     'r_emailaddress',
                     'rw_company_admin',
                     'w_share']
    )

    return linkedin_auth.authorization_url


def get_access_token_from_url(consumer_key, consumer_secret, response_url, return_url=LINKEDIN_RETURN_URL):
    linkedin_auth = LinkedInAuthentication(
        consumer_key,
        consumer_secret,
        return_url,
        permissions=['r_basicprofile',
                     'r_emailaddress',
                     'rw_company_admin',
                     'w_share']
    )

    # TODO Use url query string parser everywhere
    from urllib import parse
    v_code = parse.parse_qs(parse.urlparse(response_url).query)['code'][0]

    linkedin_auth.authorization_code = v_code
    result = linkedin_auth.get_access_token()
    return result.access_token


class LinkedIn(SocialMedia):
    def __init__(self, client_id, client_secret, oauth=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = oauth
        self.linkedin_api = LinkedInApplication(token=self.oauth_token)

    def publish_update(self, message):
        self.linkedin_api.submit_share(message)

    def publish_update_with_attachment(self, message="", name_att="", link_att="",
                                       caption_att="",
                                       description_att=""):
        self.linkedin_api.submit_share(message, name_att, description_att,
                                       link_att)

    def publish_update_with_image_attachment(self, message="", name_att="", link_att="",
                                             caption_att="",
                                             description_att="",
                                             image_url=""):
        self.linkedin_api.submit_share(message, name_att, description_att,
                                       link_att, image_url)


def main():
    url = get_authorization_url(LINKEDIN_CLIENT_ID,
                                LINKEDIN_CLIENT_SECRET)
    print(url)
    link = input("Enter Link:")
    auth_token = get_access_token_from_url(LINKEDIN_CLIENT_ID,
                                           LINKEDIN_CLIENT_SECRET, link)

    linkedin_poster = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, auth_token)

    linkedin_poster.publish_update("Only Update")

    linkedin_poster.publish_update_with_attachment("Update with Attachment",
                                                   "name_att", "link_att",
                                                   "caption_att",
                                                   "description_att")

    linkedin_poster.publish_update_with_image_attachment("Update with Image Attachment",
                                                         "name_att", "link_att",
                                                         "caption_att",
                                                         "description_att",
                                                         "image_url")


if __name__ == '__main__':
    main()
