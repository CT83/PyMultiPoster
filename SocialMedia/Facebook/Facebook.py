import facebook

from SocialMedia.SocialMedia import SocialMedia


class Facebook(SocialMedia):
    def __init__(self, client_id, client_secret, oauth=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = oauth

    def publish_update(self, message):
        graph = facebook.GraphAPI(self.oauth_token)
        graph.put_wall_post(message=message)

    def publish_update_with_attachment(self, message="", name_att="", link_att="", caption_att="",
                                       description_att=""):
        graph = facebook.GraphAPI(self.oauth_token)
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
        graph = facebook.GraphAPI(self.oauth_token)
        attachment = {
            'name': name_att,
            'link': link_att,
            'caption': caption_att,
            'description': description_att,
            'picture': image_url
        }
        graph.put_wall_post(message=message, attachment=attachment)


def main():
    # facebook_user = Facebook("101206834030831", "9be8d03bb48f86245d2bad7269831f51")
    facebook_user = Facebook("101206834030831",
                             "9be8d03bb48f86245d2bad7269831f51",
                             'EAABcDA1kKO8BAL2UjxRRJoRaX0l8usEKZCZBLxjS5k59LeKyirkfomkqElyqZBJRmWMwYcbjLDSESZB0QsTUZAAoWgwcZBXOnaRTqYZAzRqsAZAmH9g0aYmpYeBSvfjkAaNdZAXvNuzWnVBSBq9cj4xCsz6JHZC3yDrpX6nWQvrlD66ZCmsabAckjMb4vNhpWGvgcRslhHwxYADPAZDZD')
    # facebook_user.get_oauth_token(input("Facebook Code:"))
    # Get the auth token using the JS in the template folder, and input it here.
    facebook_user.publish_update("Post 1")
