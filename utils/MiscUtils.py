from CONSTANT import FACEBOOK_NAME, INSTAGRAM_NAME, TWITTER_NAME, TUMBLR_NAME, LINKEDIN_NAME, FACEBOOK_CLIENT_ID, \
    FACEBOOK_CLIENT_SECRET, LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET, \
    TUMBLR_CLIENT_ID, TUMBLR_CLIENT_SECRET
from SocialMedia.Facebook.Facebook import Facebook
from SocialMedia.LinkedIn.LinkedIn import LinkedIn
from SocialMedia.Tumblr.Tumblr import Tumblr
from SocialMedia.Twitter.Twitter import Twitter


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


def get_random_string():
    from datetime import datetime
    import random
    rand_filename = str(datetime.now()) + str(random.randint(1, 101))
    rand_filename = make_safe_filename(rand_filename)
    return rand_filename


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")


def get_all_signed_usernames(stored_cred):
    try:
        facebook_user = Facebook(FACEBOOK_CLIENT_ID,
                                 FACEBOOK_CLIENT_SECRET,
                                 stored_cred['facebook_access_token'])
        facebook_status = facebook_user.get_profile_name()
    except:
        facebook_status = None
    try:
        linkedin_poster = LinkedIn(LINKEDIN_CLIENT_ID,
                                   LINKEDIN_CLIENT_SECRET,
                                   stored_cred['linkedin_access_token'])
        linkedin_status = linkedin_poster.get_profile_name()

    except:
        linkedin_status = None
    try:
        twitter_poster = Twitter(TWITTER_CLIENT_ID,
                                 TWITTER_CLIENT_SECRET,
                                 stored_cred['twitter_access_token'],
                                 stored_cred['twitter_access_secret'])
        twitter_status = twitter_poster.get_profile_name()

    except Exception as e:
        print(e)
        twitter_status = None
    try:
        tumblr_poster = Tumblr(TUMBLR_CLIENT_ID,
                               TUMBLR_CLIENT_SECRET,
                               stored_cred['tumblr_access_token'],
                               stored_cred['tumblr_access_secret'])
        tumblr_status = tumblr_poster.get_profile_name()

    except Exception as e:
        print(e)
        tumblr_status = None
    return facebook_status, linkedin_status, tumblr_status, twitter_status
