from linkedin.linkedin import LinkedInApplication, LinkedInAuthentication

from CONSTANT import LINKEDIN_CLIENT_SECRET, LINKEDIN_CLIENT_ID, LINKEDIN_RETURN_URL, IMGUR_CLIENT_ID
from Imgur.Imgur import upload_to_imgur
from SocialMedia.SocialMedia import SocialMedia


class LinkedInAuth:
    def __init__(self, consumer_key, consumer_secret, return_url):
        self.return_url = return_url
        self.consumer_secret = consumer_secret
        self.consumer_key = consumer_key

    def get_authorization_url(self):
        linkedin_auth = LinkedInAuthentication(
            self.consumer_key,
            self.consumer_secret,
            self.return_url,
            permissions=['r_basicprofile',
                         'r_emailaddress',
                         'rw_company_admin',
                         'w_share']
        )

        return linkedin_auth.authorization_url

    def get_access_token_from_url(self, response_url):
        linkedin_auth = LinkedInAuthentication(
            self.consumer_key,
            self.consumer_secret,
            self.return_url,
            permissions=['r_basicprofile',
                         'r_emailaddress',
                         'rw_company_admin',
                         'w_share']
        )

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

    def publish_update(self, message, title=""):
        self.linkedin_api.submit_share(title, message)

    def publish_update_with_attachment(self, message="", name_att="", link_att="",
                                       caption_att="",
                                       description_att=""):
        self.linkedin_api.submit_share(message, name_att, description_att,
                                       link_att)

    def publish_update_with_image_attachment(self, message="", image_url="", link_att="",
                                             caption_att="", description_att="",
                                             title=""):
        if link_att in "":
            link_att = image_url
        self.linkedin_api.submit_share(message, title, description_att,
                                       link_att, image_url)

    def convert_publish_update_with_image_attachment(self, message="", image_url="",
                                                     title=""):
        image_url = upload_to_imgur(IMGUR_CLIENT_ID, image_url)
        print("Linkedin Uploaded Image:", image_url)
        self.linkedin_api.submit_share(message, title, "", image_url, image_url)


def main():
    linkedin_auth = LinkedInAuth(LINKEDIN_CLIENT_ID,
                                 LINKEDIN_CLIENT_SECRET,
                                 LINKEDIN_RETURN_URL)

    print(linkedin_auth.get_authorization_url())
    link = input("Enter Link:")
    auth_token = linkedin_auth.get_access_token_from_url(link)

    linkedin_poster = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, auth_token)

    linkedin_poster.publish_update("Only Update")

    linkedin_poster.publish_update_with_attachment("Update with Attachment",
                                                   "name_att", "link_att",
                                                   "caption_att",
                                                   "description_att")
    image_url = upload_to_imgur(IMGUR_CLIENT_ID, 'temp.jpg')
    linkedin_poster.publish_update_with_image_attachment(
        title="Title", image_url=image_url, message="Update with Image Attachment")


if __name__ == '__main__':
    main()
