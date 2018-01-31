from linkedin.linkedin import LinkedInAuthentication, LinkedInApplication


def main():
    CLIENT_ID = '81spnwn20ee6ve'
    CLIENT_SECRET = '0Yg845bXH8Z3K4Sf'
    RETURN_URL = 'https://pymultiposter.herokuapp.com/'

    authentication = LinkedInAuthentication(
        CLIENT_ID,
        CLIENT_SECRET,
        RETURN_URL,
        permissions=['r_basicprofile',
                     'r_emailaddress',
                     'rw_company_admin',
                     'w_share']
    )

    print(authentication.authorization_url)
    authentication.authorization_code = input('Result=')
    result = authentication.get_access_token()
    print("Access Token:", result.access_token)
    print("Expires in (seconds):", result.expires_in)
    # TODO Refactor this to something better
    lkin_api = LinkedInApplication(token=result.access_token)
    # submit_share(self, comment=None, title=None, description=None,submitted_url=None,submitted_image_url=None,visibility_code='anyone'):
    print(lkin_api.submit_share('Posting from the API using JSON2',
                                'A title for your share', None,
                                'https://www.linkedin.com'))


if __name__ == '__main__':
    main()
