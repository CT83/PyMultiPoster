from linkedin.linkedin import LinkedInApplication, LinkedInAuthentication

from CONSTANT import LINKEDIN_CLIENT_SECRET, LINKEDIN_CLIENT_ID, LINKEDIN_RETURN_URL
from SocialMedia.SocialMedia import SocialMedia


def get_link():
    authentication = LinkedInAuthentication(
        LINKEDIN_CLIENT_ID,
        LINKEDIN_CLIENT_SECRET,
        LINKEDIN_RETURN_URL,
        permissions=['r_basicprofile',
                     'r_emailaddress',
                     'rw_company_admin',
                     'w_share']
    )

    url = authentication.authorization_url
    print(authentication.authorization_url)
    authentication.authorization_code = input('Result=')
    result = authentication.get_access_token()
    print("Access Token:", result.access_token)
    print("Expires in (seconds):", result.expires_in)
    lkin_api = LinkedInApplication(token=result.access_token)
    print(lkin_api.submit_share('Posting from the API using JSON2',
                                'A title for your share', None,
                                'https://www.linkedin.com'))
    return url


def get_code():
    authentication = LinkedInAuthentication(
        LINKEDIN_CLIENT_ID,
        LINKEDIN_CLIENT_SECRET,
        LINKEDIN_RETURN_URL,
        permissions=['r_basicprofile',
                     'r_emailaddress',
                     'rw_company_admin',
                     'w_share']
    )
    print(authentication.authorization_url)
    authentication.authorization_code = input('Result=')
    result = authentication.get_access_token()
    code = result.access_token
    print("Access Token:", result.access_token)
    print("Expires in (seconds):", result.expires_in)
    lkin_api = LinkedInApplication(token=result.access_token)
    print(lkin_api.submit_share('Posting from the API using JSON2',
                                'A title for your share', None,
                                'https://www.linkedin.com'))
    return code


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
    linkedin_poster = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, get_code())
    try:
        linkedin_poster.publish_update("Only Update")
    except:
        pass

    try:
        linkedin_poster.publish_update_with_attachment("Update with Attachment",
                                                       "name_att", "link_att",
                                                       "caption_att",
                                                       "description_att")
    except:
        pass

    try:
        linkedin_poster.publish_update_with_image_attachment("Update with Image Attachment",
                                                             "name_att", "link_att",
                                                             "caption_att",
                                                             "description_att",
                                                             "image_url")
    except:
        pass


main()
