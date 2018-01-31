from SocialMedia.SocialMedia import SocialMedia


class Facebook(SocialMedia):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = ""

    def get_authorization_url(self):
        payload = {'grant_type': 'client_credentials',
                   'client_id': self.client_id,
                   'client_secret': self.client_secret}
        import requests
        file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
        return file.url

    def get_oauth_token(self, authorization_code):
        self.oauth_token = authorization_code
        return self.oauth_token


facebook = Facebook("101206834030831", "9be8d03bb48f86245d2bad7269831f51")
consent_url = facebook.get_authorization_url()
print(consent_url)
facebook.get_oauth_token(input("Facebook Code:"))
