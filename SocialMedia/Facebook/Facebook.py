import facebook

from CONSTANT import FACEBOOK_CLIENT_SECRET, FACEBOOK_CLIENT_ID
from SocialMedia.SocialMedia import SocialMedia


class Facebook(SocialMedia):
    def __init__(self, client_id, client_secret, oauth=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = oauth

    def publish_update(self, message):
        graph = facebook.GraphAPI(self.access_token)
        graph.put_wall_post(message=message)

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

    def publish_update_with_image_attachment(self, message="", name_att="", link_att="",
                                             caption_att="",
                                             description_att="",
                                             image_url=""):
        graph = facebook.GraphAPI(self.access_token)
        attachment = {
            'name': name_att,
            'link': link_att,
            'caption': caption_att,
            'description': description_att,
            'picture': image_url
        }
        graph.put_wall_post(message=message, attachment=attachment)

    def generate_long_lived_token(self):
        graph = facebook.GraphAPI(self.access_token)

        extended_token = graph.extend_access_token(self.client_id, self.client_secret)
        print(extended_token)
        return extended_token


def main():
    # facebook_user = Facebook("101206834030831", "9be8d03bb48f86245d2bad7269831f51")
    facebook_user = Facebook(FACEBOOK_CLIENT_ID,
                             FACEBOOK_CLIENT_SECRET,
                             'EAAZA1GWuwuqkBAKuldzi4z96nxPALqsNojP2IZAHWDrkRUZCKxpddjsp2eu2JSu7yov7e9nkJzAnQvfBMfwN74m7hlLpa55FlrNhwZAvFiiJeguHzSkqpp5q3pmi4Dby8RHALZB2NxTzYyUBCVEtrKgc6PIwO4L6jFCqDzukOpovqVZCNes9E1OA3DvwHA25ZAMlZBhoSwnhkwZDZD')
    # facebook_user.get_oauth_token(input("Facebook Code:"))
    # Get the auth token using the JS in the template folder, and input it here.
    # facebook_user.publish_update("Post 1")
    facebook_user.publish_update_with_image_attachment(message="Posst 1sa",
                                                       link_att='temp1.png',
                                                       image_url='temp1.png')


if __name__ == '__main__':
    main()
