import facebook

from CONSTANT import FACEBOOK_CLIENT_SECRET, FACEBOOK_CLIENT_ID
from SocialMedia.SocialMedia import SocialMedia


class Facebook(SocialMedia):
    def __init__(self, client_id, client_secret, oauth=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = oauth

        self.post_id = None

    def get_user_id_name(self):
        graph = facebook.GraphAPI(self.access_token)
        profile = graph.get_object("me")
        return profile['id']

    def get_profile_name(self):
        graph = facebook.GraphAPI(self.access_token)
        profile = graph.get_object("me")
        return profile['name']

    def publish_update(self, message, **kwargs):
        graph = facebook.GraphAPI(self.access_token)
        status = graph.put_wall_post(message=message)

        self.post_id = status['id']

    def publish_update_page(self, message, page_id=None):
        graph = facebook.GraphAPI(self.access_token)
        resp = graph.get_object('me/accounts')
        page_access_token = None
        for page in resp['data']:
            if page['id'] == page_id:
                page_access_token = page['access_token']
        graph = facebook.GraphAPI(page_access_token)
        status = graph.put_wall_post(message=message)
        self.post_id = status['id']

    def publish_update_image(self, message, image):
        import requests
        url = "https://graph.facebook.com/me/photos?access_token=" + self.access_token + "&message=" + message
        files = {'source': open(image, 'rb')}
        status = requests.post(url, files=files)
        status = dict(status.json())
        self.post_id = status['post_id']

    def publish_update_image_page(self, message, image, page_id):

        graph = facebook.GraphAPI(self.access_token)
        resp = graph.get_object('me/accounts')
        page_access_token = None
        for page in resp['data']:
            if page['id'] == page_id:
                page_access_token = page['access_token']

        import requests
        url = "https://graph.facebook.com/" + page_id + "/photos?access_token=" \
              + page_access_token + "&message=" + message
        files = {'source': open(image, 'rb')}
        status = requests.post(url, files=files)
        status = dict(status.json())
        self.post_id = status['post_id']

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
        status = graph.put_wall_post(message=message, attachment=attachment)
        self.post_id = status['id']

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
        status = graph.put_wall_post(message=message, attachment=attachment)
        self.post_id = status['id']

    def generate_long_lived_token(self):
        graph = facebook.GraphAPI(self.access_token)

        extended_token = graph.extend_access_token(self.client_id, self.client_secret)
        access_token = extended_token['access_token']
        print(access_token)
        return access_token

    def get_link_latest_post(self, post_id=None):
        """REMEMBER! This function doesn't actually return the post link; as the post link could
         not be view sometimes due to some errors, instead it returns the Profile link."""
        try:
            if post_id is None:
                # post_url = 'https://facebook.com/' + str(self.post_id).split('_', 1)[0]
                post_url = 'https://facebook.com/' + self.post_id
                return post_url
        except (TypeError, KeyError) as e:
            print(e)
            return ""


def main():
    facebook_user = Facebook(FACEBOOK_CLIENT_ID,
                             FACEBOOK_CLIENT_SECRET,
                             'EAAZA1GWuwuqkBAC6UCUUCHla86ZBJ3DOby12s6W7QefTjuETwQvVtrVmT5Vxis5ipTZConkZA9tTSu5WFiF4pTROAamN1POaL4wyvftn6h6aVg1ZAnEyD5ds7QEBL2Inkn9joufrzTS5yHVkZAPA3p5VArOa7ks9wZD')
    # Get the auth token using the JS in the template folder, and input it here.
    # facebook_user.publish_update("Post 1", page_id="328045644353380")
    # facebook_user.publish_update_with_image_attachment(message="Posst 1sa",
    #                                                    page_id="328045644353380",
    #                                                    link_att='temp1.png',
    #                                                    image_url='temp1.png')
    facebook_user.get_user_id_name()
    facebook_user.publish_update_image_page(message="Posst 1sa",
                                            page_id="328045644353380",
                                            image='temp1.png')


if __name__ == '__main__':
    main()
