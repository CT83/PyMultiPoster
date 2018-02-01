from SocialMedia.SocialMedia import SocialMedia
import facebook


class Facebook(SocialMedia):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = ""


    def publish_update(self, message):
        graph = facebook.GraphAPI(self.oauth_token)
        graph.put_wall_post(message=message)


facebook_user = Facebook("101206834030831", "9be8d03bb48f86245d2bad7269831f51")
# consent_url = facebook_user.get_authorization_url()
# print(consent_url)
# facebook_user.get_oauth_token(input("Facebook Code:"))
# Get the auth token using the JS in the template folder, and input it here.
facebook_user.oauth_token ='EAABcDA1kKO8BAL2UjxRRJoRaX0l8usEKZCZBLxjS5k59LeKyirkfomkqElyqZBJRmWMwYcbjLDSESZB0QsTUZAAoWgwcZBXOnaRTqYZAzRqsAZAmH9g0aYmpYeBSvfjkAaNdZAXvNuzWnVBSBq9cj4xCsz6JHZC3yDrpX6nWQvrlD66ZCmsabAckjMb4vNhpWGvgcRslhHwxYADPAZDZD'
facebook_user.publish_update("Post 1")
