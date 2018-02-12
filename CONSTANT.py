# Initializers
import os

ON_HEROKU = 'ON_HEROKU' in os.environ

# Tumblr
TUMBLR_CLIENT_ID = "h8QTvJw4B8xMDo9GAFXC8Ll7xbX99MUhDiIA7AFBIfH2cuNzy3"
TUMBLR_CLIENT_SECRET = "g8Kgg8fIm8W8YadqqJy5mKR0dzUGYQXYwg1GvNHLofpgmohQoe"
TUMBLR_REDIRECT_URL='http://localhost:5000/tumblr_redirect'

# Facebook App pymultiposter
# FACEBOOK_CLIENT_ID = "101206834030831"
# FACEBOOK_CLIENT_SECRET = "9be8d03bb48f86245d2bad7269831f51"


if ON_HEROKU:
    # # Facebook App pymultiposter-2
    FACEBOOK_CLIENT_ID = "2061306277447865"
    FACEBOOK_CLIENT_SECRET = "965931cb788a2268bd5c2545335042a0"

    # LinkedIn
    LINKEDIN_RETURN_URL = 'https://pymultiposter-2.herokuapp.com/linkedin_redirect'
    LINKEDIN_CLIENT_ID = '81spnwn20ee6ve'
    LINKEDIN_CLIENT_SECRET = '0Yg845bXH8Z3K4Sf'

else:
    # Facebook App pymultiposter-local
    FACEBOOK_CLIENT_ID = "1817601901640361"
    FACEBOOK_CLIENT_SECRET = "ee3029327b955fac864c7d3eb1c139ae"

    # LinkedIn
    LINKEDIN_RETURN_URL = 'http://localhost:5000/linkedin_redirect'
    LINKEDIN_CLIENT_ID = '81spnwn20ee6ve'
    LINKEDIN_CLIENT_SECRET = '0Yg845bXH8Z3K4Sf'

    # Twitter
    TWITTER_CLIENT_ID = "ecf8Ygwl3Sr9te5dvHoknoq7h"
    TWITTER_CLIENT_SECRET = 'xM7G3WocNnSYRCsIsJw7yeRDasuJ3QzxdRlS7iLZoVr92gKtAg'
    TWITTER_REDIRECT_URL='http://localhost:5000/twitter_redirect'
