from linkedin.linkedin import LinkedInApplication, LinkedInAuthentication

from CONSTANT import LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET
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
    # TODO Fix Linkedin .submit_share(comment, description) confusion
    def __init__(self, client_id, client_secret, oauth=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = oauth
        self.linkedin_api = LinkedInApplication(token=self.oauth_token)

        self.post_url = None

    def publish_update(self, message, title=""):
        status = self.linkedin_api.submit_share(title=title, comment=title + " " + message)
        self.post_url = status['updateUrl']

    def publish_update_with_attachment(self, message="", name_att="", link_att="",
                                       caption_att="",
                                       description_att=""):
        status = self.linkedin_api.submit_share(message, name_att, description_att,
                                                link_att)
        self.post_url = status['updateUrl']

    def publish_update_with_image_attachment(self, message="", image_url="", link_att="",
                                             caption_att="", description_att="",
                                             title=""):
        if link_att in "":
            link_att = image_url
        status = self.linkedin_api.submit_share(message, title, description_att,
                                                link_att, image_url)
        self.post_url = status['updateUrl']

    def publish_update_company_page(self, message="", title="", company_id="",
                                    submitted_url="",
                                    submitted_image_url=""):
        import requests
        from flask import json

        json_d = {
            "visibility": {"code": "anyone"},
            "comment": message,
        }
        if submitted_url or submitted_image_url:
            json_d["content"] = {
                "submitted-­url": submitted_url,
                "title": title,
                "description": message,
                "submitted‐image-­url": submitted_image_url
            }

        json_j = json.dumps(json_d)
        auth = self.oauth_token.strip()
        url = "https://api.linkedin.com/v1/companies/{}" \
              "/shares?oauth2_access_token={}" \
              "&format=json".format(company_id, auth)
        header = {'Content-Type': 'application/json',
                  "x-li-format": "json",
                  'Connection': 'Keep-Alive'
                  }

        status = requests.post(url, headers=header, data=json_j)
        status = dict(status.json())

        url = "https://www.linkedin.com/feed/update/urn:li:activity:{}/" \
            .format(status['updateKey'].split('-')[-1])

        self.post_url = url
        return self.post_url

    def get_link_latest_post(self):
        return self.post_url

    def get_profile_name(self):
        profile = self.linkedin_api.get_profile()
        return profile['firstName'] + " " + profile['lastName']


def main():
    # linkedin_auth = LinkedInAuth(LINKEDIN_CLIENT_ID,
    #                              LINKEDIN_CLIENT_SECRET,
    #                              LINKEDIN_RETURN_URL)
    #
    # print(linkedin_auth.get_authorization_url())
    # link = input("Enter Link:")
    # auth_token = linkedin_auth.get_access_token_from_url(link)
    #
    linkedin_poster = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET,
                               "AQVwWpDvP_2FTR5hvTHRXNbMKlWh5sK9BDVJmKG_fzAnKKgoT6bLDrZy0z3kN-RQa2e36evsfTMMlw4gq5BwlQiBbWUq7JIZAxALCssZ4nPPdeKFlEfnehh8Qqw87_eu6-ulyVPdWEsgS-zAxpNQPRW5IlJ2tQ56Lk_jGMlnnVowikarEfCs4VIqBo1GxP8YouYpefmwK_Yebelp-VFeRCpNJ3Nx1dAeLn3d5cRNyXE8nrvDYfqxSSQrtWewiNz1u9QUS-2wmOrLXjfJSfUuOM-stOi4Cbzcnrsh9xljamU9SKj-WjGQLFjfFEMqY-K3_-4aEAODYdzto-3rIAAzV6i6YInb4w")
    print(linkedin_poster.get_profile_name())
    linkedin_poster.publish_update_company_page(message="Test23 Message",
                                                title="Title Message",
                                                company_id="13691092",
                                                # submitted_url="https://www.google.com",
                                                # submitted_image_url="https://example.com/example.jpg")
                                                )

    # linkedin_poster.publish_update("Only Updatesa")
    #
    # linkedin_poster.publish_update_with_attachment("Update with Attachment",
    #                                                "name_att", "link_att",
    #                                                "caption_att",
    #                                                "description_att")
    # image_url = upload_to_imgur(IMGUR_CLIENT_ID, 'temp.jpg')
    # linkedin_poster.publish_update_with_image_attachment(
    #     title="Title", image_url=image_url, message="Update with Image Attachment")


if __name__ == '__main__':
    main()
