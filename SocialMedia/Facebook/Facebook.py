import facebook

from CONSTANT import FACEBOOK_CLIENT_SECRET, FACEBOOK_CLIENT_ID
from SocialMedia.SocialMedia import SocialMedia


class Facebook(SocialMedia):
    def __init__(self, client_id, client_secret, oauth=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = oauth

    def publish_update(self, message, **kwargs):
        graph = facebook.GraphAPI(self.access_token)
        graph.put_wall_post(message=message)

    def publish_update_page(self, message, page_id=None):
        graph = facebook.GraphAPI(self.access_token)
        resp = graph.get_object('me/accounts')
        page_access_token = None
        for page in resp['data']:
            if page['id'] == page_id:
                page_access_token = page['access_token']
        graph = facebook.GraphAPI(page_access_token)
        print(graph.put_wall_post(message=message))

    def publish_update_image(self, message, image):
        import requests
        url = "https://graph.facebook.com/me/photos?access_token=" + self.access_token + "&message=" + message
        files = {'source': open(image, 'rb')}
        requests.post(url, files=files)

    def publish_update_with_attachment(self, message="", name_att="", link_att="",
                                       caption_att="",
                                       description_att=""):
        graph = facebook.GraphAPI(self.access_token)
        attachment = {
            'name': name_att,
            'link': link_att,
            'caption': caption_att,
            'description': description_att,
        }
        graph.put_wall_post(message=message, attachment=attachment)

    def publish_update_with_image_attachment(self, message, image_url,
                                             name_att="", link_att="", caption_att="",
                                             description_att=""):
        if link_att in "":
            link_att = image_url

        graph = facebook.GraphAPI(self.access_token)
        attachment = {
            'name': name_att,
            'link': link_att,
            'caption': caption_att,
            'description': description_att,
            'picture': image_url
        }
        graph.put_wall_post(message=message, attachment=attachment)

    def publish_update_with_image_attachment_page(self, message, image_url, page_id,
                                                  link_att=""):
        if link_att in "":
            link_att = image_url

        graph = facebook.GraphAPI(self.access_token)
        attachment = {
            'link': link_att,
            'picture': image_url
        }

        resp = graph.get_object('me/accounts')
        page_access_token = None
        for page in resp['data']:
            if page['id'] == page_id:
                page_access_token = page['access_token']
        graph = facebook.GraphAPI(page_access_token)
        print(graph.put_wall_post(message=message, attachment=attachment))

    def generate_long_lived_token(self):
        graph = facebook.GraphAPI(self.access_token)

        extended_token = graph.extend_access_token(self.client_id, self.client_secret)
        access_token = extended_token['access_token']
        print(access_token)
        return access_token


def main():
    facebook_user = Facebook(FACEBOOK_CLIENT_ID,
                             FACEBOOK_CLIENT_SECRET,
                             'EAAZA1GWuwuqkBAKuldzi4z96nxPALqsNojP2IZAHWDrkRUZCKxpddjsp2eu2JSu7yov7e9nkJzAnQvfBMfwN74m7hlLpa55FlrNhwZAvFiiJeguHzSkqpp5q3pmi4Dby8RHALZB2NxTzYyUBCVEtrKgc6PIwO4L6jFCqDzukOpovqVZCNes9E1OA3DvwHA25ZAMlZBhoSwnhkwZDZD')
    # Get the auth token using the JS in the template folder, and input it here.
    facebook_user.publish_update("Post 1", page_id="328045644353380")
    # facebook_user.publish_update_with_image_attachment(message="Posst 1sa",
    #                                                    page_id="328045644353380",
    #                                                    link_att='temp1.png',
    #                                                    image_url='temp1.png')


if __name__ == '__main__':
    main()
