def get_cookie(req):
    facebook_access_token = req.cookies.get('FACEBOOK_ACCESS_TOKEN')

    twitter_access_token = req.cookies.get('TWITTER_ACCESS_TOKEN')
    twitter_access_secret = req.cookies.get('TWITTER_ACCESS_SECRET')

    instagram_email = req.cookies.get('INSTAGRAM_EMAIL')
    instagram_password = req.cookies.get('INSTAGRAM_PASSWORD')

    linkedin_access_token = req.cookies.get('LINKEDIN_ACCESS_TOKEN')

    tumblr_access_token = req.cookies.get('TUMBLR_ACCESS_TOKEN')
    tumblr_access_secret = req.cookies.get('TUMBLR_ACCESS_SECRET')

    return facebook_access_token, twitter_access_token, \
           twitter_access_secret, instagram_email, \
           instagram_password, linkedin_access_token, \
           tumblr_access_token, tumblr_access_secret


def set_cookie(resp, facebook_access_token, twitter_access_token,
               twitter_access_secret, instagram_email, instagram_password,
               linkedin_access_token, tumblr_access_token,
               tumblr_access_secret):
    resp.set_cookie('FACEBOOK_ACCESS_TOKEN', facebook_access_token)

    resp.set_cookie('TWITTER_ACCESS_TOKEN', twitter_access_token)
    resp.set_cookie('TWITTER_ACCESS_SECRET', twitter_access_secret)

    resp.set_cookie('INSTAGRAM_EMAIL', instagram_email)
    resp.set_cookie('INSTAGRAM_PASSWORD', instagram_password)

    resp.set_cookie('LINKEDIN_ACCESS_TOKEN', linkedin_access_token)

    resp.set_cookie('TUMBLR_ACCESS_TOKEN', tumblr_access_token)
    resp.set_cookie('TUMBLR_ACCESS_SECRET', tumblr_access_secret)
