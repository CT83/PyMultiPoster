import requests


def get_fb_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
    print(file.url)
    # print file.text #to test what the FB api responded with
    # result = file.text.split("=")[1]
    # print file.text #to test the TOKEN
    return file.text

    print(get_fb_token("101206834030831", "9be8d03bb48f86245d2bad7269831f51"))
# https://www.facebook.com/v2.11/dialog/oauth?client_id={162435237720033}&redirect_uri={"https://pyreserver.herokuapp.com/database_admin_s"}&state={"{st=state123abc,ds=123456789}"}
# https://www.facebook.com/v2.11/dialog/oauth?client_id={162435237720033}&redirect_uri={"https://www.getpostman.com/oauth2/callback"}&state={"{st=state123abc,ds=123456789}"}
# https://www.facebook.com/v2.11/dialog/oauth?client_id={101206834030831}&redirect_uri={"http://localhost/"}&state={"{st=state123abc,ds=123456789}"}
