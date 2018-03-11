from CONSTANT import FACEBOOK_NAME, INSTAGRAM_NAME, TWITTER_NAME, TUMBLR_NAME, LINKEDIN_NAME


def get_signed_social(user):
    """This function searches for the name of the social network in stored
    credentials, the get_cookie() function returns a dict. of credentials. This
    function checks the names of social networks against the names of the
    returned dict. keys and the returns a list of found items.
    It is used to show which social networks have cookie keys associated with them.
    """
    signed_social = []
    from models.Credentials import get_credentials
    credentials = get_credentials(user)
    credentials = {k: v for k, v in credentials.items() if v is not None}
    for key in credentials.keys():
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
