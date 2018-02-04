from linkedin.linkedin import LinkedInApplication, LinkedInAuthentication

from CONSTANT import LINKEDIN_CLIENT_SECRET, LINKEDIN_CLIENT_ID, LINKEDIN_RETURN_URL
from SocialMedia.SocialMedia import SocialMedia


def get_code(authentication, auth_code):
    print(auth_code)
    authentication.authorization_code = auth_code
    result = authentication.get_access_token()
    code = result.access_token
    print("Access Token:", result.access_token)
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
    linkedin_auth = LinkedInAuthentication(
        LINKEDIN_CLIENT_ID,
        LINKEDIN_CLIENT_SECRET,
        LINKEDIN_RETURN_URL,
        permissions=['r_basicprofile',
                     'r_emailaddress',
                     'rw_company_admin',
                     'w_share']
    )

    print(linkedin_auth.authorization_url)
    link = input("Enter Code from Link:")
    code = get_code(linkedin_auth, link)

    linkedin_poster = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, code)
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


main()
