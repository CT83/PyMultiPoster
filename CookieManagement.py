def get_cookie(req):
    facebook_access_token = req.cookies.get('FACEBOOK_ACCESS_TOKEN')

    twitter_access_token = req.cookies.get('TWITTER_ACCESS_TOKEN')
    twitter_access_secret = req.cookies.get('TWITTER_ACCESS_SECRET')

    instagram_email = req.cookies.get('INSTAGRAM_EMAIL')
    instagram_password = req.cookies.get('INSTAGRAM_PASSWORD')

    linkedin_access_token = req.cookies.get('LINKEDIN_ACCESS_TOKEN')

    tumblr_access_token = req.cookies.get('TUMBLR_ACCESS_TOKEN')
    tumblr_access_secret = req.cookies.get('TUMBLR_ACCESS_SECRET')

    stored_cookies = {'facebook_access_token': facebook_access_token,
                      'twitter_access_token': twitter_access_token,
                      'twitter_access_secret': twitter_access_secret,
                      'instagram_email': instagram_email,
                      'instagram_password': instagram_password,
                      'linkedin_access_token': linkedin_access_token,
                      'tumblr_access_token': tumblr_access_token,
                      'tumblr_access_secret': tumblr_access_secret}

    return stored_cookies


def set_cookie(resp, facebook_access_token="", twitter_access_token="",
               twitter_access_secret="", instagram_email="", instagram_password="",
               linkedin_access_token="", tumblr_access_token="",
               tumblr_access_secret=""):
    if facebook_access_token:
        resp.set_cookie('FACEBOOK_ACCESS_TOKEN', facebook_access_token)

    if twitter_access_token and twitter_access_secret:
        resp.set_cookie('TWITTER_ACCESS_TOKEN', twitter_access_token)
        resp.set_cookie('TWITTER_ACCESS_SECRET', twitter_access_secret)

    if instagram_email and instagram_password:
        resp.set_cookie('INSTAGRAM_EMAIL', instagram_email)
        resp.set_cookie('INSTAGRAM_PASSWORD', instagram_password)

    if linkedin_access_token:
        resp.set_cookie('LINKEDIN_ACCESS_TOKEN', linkedin_access_token)

    if tumblr_access_token and tumblr_access_secret:
        resp.set_cookie('TUMBLR_ACCESS_TOKEN', tumblr_access_token)
        resp.set_cookie('TUMBLR_ACCESS_SECRET', tumblr_access_secret)
    return resp
