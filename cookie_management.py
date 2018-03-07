from CONSTANT import FACEBOOK_NAME, LINKEDIN_NAME, TUMBLR_NAME, TWITTER_NAME, INSTAGRAM_NAME


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


def delete_all_cookies(resp):
    print("All cookies have been deleted.")
    resp.set_cookie('FACEBOOK_ACCESS_TOKEN', expires=0)
    resp.set_cookie('TWITTER_ACCESS_TOKEN', expires=0)
    resp.set_cookie('TWITTER_ACCESS_SECRET', expires=0)
    resp.set_cookie('INSTAGRAM_EMAIL', expires=0)
    resp.set_cookie('INSTAGRAM_PASSWORD', expires=0)
    resp.set_cookie('LINKEDIN_ACCESS_TOKEN', expires=0)
    resp.set_cookie('TUMBLR_ACCESS_TOKEN', expires=0)
    resp.set_cookie('TUMBLR_ACCESS_SECRET', expires=0)
    return resp


def get_signed_social(req):
    """This function searches for the name of the social network in stored
    cookies, the get_cookie() function returns a dict. of cookies. This
    function checks the names of social networks against the names of the
    returned dict. keys and the returns a list of found items.
    It is used to show which social networks have cookie keys associated with them.
    """
    signed_social = []
    cookies = get_cookie(req)
    cookies = {k: v for k, v in cookies.items() if v is not None}
    for key in cookies.keys():
        if FACEBOOK_NAME.lower() in key.lower():
            signed_social.append(FACEBOOK_NAME)
        if INSTAGRAM_NAME.lower() in key.lower():
            signed_social.append(INSTAGRAM_NAME)
        if TWITTER_NAME.lower() in key.lower():
            signed_social.append(TWITTER_NAME)
        if TUMBLR_NAME.lower() in key.lower():
            signed_social.append(TUMBLR_NAME)
        if LINKEDIN_NAME.lower() in key.lower():
            signed_social.append(LINKEDIN_NAME)
    signed_social = list(set(signed_social))
    print("Signed in Social Networks:", signed_social)
    return signed_social
