import tweepy

CONSUMER_KEY = 'ecf8Ygwl3Sr9te5dvHoknoq7h'
CONSUMER_SECRET = 'xM7G3WocNnSYRCsIsJw7yeRDasuJ3QzxdRlS7iLZoVr92gKtAg'
ACCESS_TOKEN = '957098797791768576-iBgwacSqxbsFM3cah3fndBjndLm8eOO'
ACCESS_TOKEN_SECRET = '7VNkIwputPvlhWhBnltCJu9Ct9INAN5vOfgtls00YtF8x'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
try:
    redirect_url = auth.get_authorization_url()
    print("Redirect URL", str(redirect_url))
except tweepy.TweepError:
    print('Error! Failed to get request token.')
print(auth.request_token)
token = auth.request_token

# Let's say this is a web app, so we need to re-build the auth handler
# first...
verifier = input('Verifier:')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.request_token = token
try:
    auth.get_access_token(verifier)
    print('Got access!!')
    api = tweepy.API(auth)
    api.update_status(status="Sent fomre ")
except tweepy.TweepError:
    print('Error! Failed to get access token.')
