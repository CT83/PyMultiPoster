import requests

# Note: This only works for Apps and not for generating the oauth tokens for users, and showing them the allow app to access facebook dialog.

def get_fb_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
    print(file.url)
    return file


print(get_fb_token("101206834030831", "9be8d03bb48f86245d2bad7269831f51"))
