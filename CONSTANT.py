# Initializers
import os

ON_HEROKU = 'ON_HEROKU' in os.environ

# Facebook App pymultiposter
# FACEBOOK_CLIENT_ID = "101206834030831"
# FACEBOOK_CLIENT_SECRET = "9be8d03bb48f86245d2bad7269831f51"

IMGUR_CLIENT_ID = "3f4360ea159fad4"
IMGUR_CLIENT_SECRET = "be5c53e8daf8645f2f33c3b9d8c8ac9488396fb6"

S3_BUCKET = "pymultiposter-2"
S3_KEY = "AKIAJEYHDBZNM4XQTOHA"
S3_SECRET = "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"

if ON_HEROKU:
    # # Facebook App pymultiposter-2
    FACEBOOK_CLIENT_ID = "2061306277447865"
    FACEBOOK_CLIENT_SECRET = "965931cb788a2268bd5c2545335042a0"

    # LinkedIn
    LINKEDIN_RETURN_URL = 'https://pymultiposter-2.herokuapp.com/linkedin_redirect'
    LINKEDIN_CLIENT_ID = '81spnwn20ee6ve'
    LINKEDIN_CLIENT_SECRET = '0Yg845bXH8Z3K4Sf'
    # LINKEDIN_CLIENT_ID = '81yloqxu0xgoeo'
    # LINKEDIN_CLIENT_SECRET = 'wyElIY59DrZwTRIA'

    # Twitter
    TWITTER_CLIENT_ID = "ecf8Ygwl3Sr9te5dvHoknoq7h"
    TWITTER_CLIENT_SECRET = 'xM7G3WocNnSYRCsIsJw7yeRDasuJ3QzxdRlS7iLZoVr92gKtAg'
    TWITTER_REDIRECT_URL = 'https://pymultiposter-2.herokuapp.com/twitter_redirect'

    # Tumblr
    TUMBLR_CLIENT_ID = "h8QTvJw4B8xMDo9GAFXC8Ll7xbX99MUhDiIA7AFBIfH2cuNzy3"
    TUMBLR_CLIENT_SECRET = "g8Kgg8fIm8W8YadqqJy5mKR0dzUGYQXYwg1GvNHLofpgmohQoe"
    TUMBLR_REDIRECT_URL = 'https://pymultiposter-2.herokuapp.com/tumblr_redirect'

    UPLOAD_PATH = "/tmp/"
else:
    # Facebook App pymultiposter-local
    FACEBOOK_CLIENT_ID = "1817601901640361"
    FACEBOOK_CLIENT_SECRET = "ee3029327b955fac864c7d3eb1c139ae"

    # LinkedIn
    LINKEDIN_RETURN_URL = 'http://localhost:5000/linkedin_redirect'
    # LINKEDIN_CLIENT_ID = '81spnwn20ee6ve'
    # LINKEDIN_CLIENT_SECRET = '0Yg845bXH8Z3K4Sf'
    LINKEDIN_CLIENT_ID = '81yloqxu0xgoeo'
    LINKEDIN_CLIENT_SECRET = 'wyElIY59DrZwTRIA'

    # Twitter
    TWITTER_CLIENT_ID = "ecf8Ygwl3Sr9te5dvHoknoq7h"
    TWITTER_CLIENT_SECRET = 'xM7G3WocNnSYRCsIsJw7yeRDasuJ3QzxdRlS7iLZoVr92gKtAg'
    TWITTER_REDIRECT_URL = 'http://localhost:5000/twitter_redirect'

    # Tumblr
    TUMBLR_CLIENT_ID = "h8QTvJw4B8xMDo9GAFXC8Ll7xbX99MUhDiIA7AFBIfH2cuNzy3"
    TUMBLR_CLIENT_SECRET = "g8Kgg8fIm8W8YadqqJy5mKR0dzUGYQXYwg1GvNHLofpgmohQoe"
    TUMBLR_REDIRECT_URL = 'http://localhost:5000/tumblr_redirect'

    UPLOAD_PATH = "uploads/"

TWITTER_NAME = 'Twitter'
FACEBOOK_NAME = 'Facebook'
TUMBLR_NAME = 'Tumblr'
INSTAGRAM_NAME = 'Instagram'
LINKEDIN_NAME = 'Linkedin'

SUPPORTED_SOCIAL_NETWORKS = [FACEBOOK_NAME,
                             INSTAGRAM_NAME,
                             TUMBLR_NAME,
                             LINKEDIN_NAME,
                             TWITTER_NAME]

AWS_RDS_URL = "postgresql://administrator:cybertech83@pymultiposter-common-queue.c44vnyfhjrjn.us-east-1.rds.amazonaws.com:5432/postgres"

LOCALHOST_POSTGRES = "postgresql://postgres:cybertech83@localhost/postgres"
