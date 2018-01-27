import requests


def get_fb_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
    # print file.text #to test what the FB api responded with
    # result = file.text.split("=")[1]
    # print file.text #to test the TOKEN
    return file.text


print(get_fb_token("162435237720033", "cd7e9f7e2d4655bc17211a5c02334d3a"))
