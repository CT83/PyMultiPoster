from linkedin.linkedin import LinkedInAuthentication, LinkedInApplication
import sys, os


class LinkedInWrapper(object):
    def __init__(self, id, secret, port, auth_token=None, auth_code=None):
        self.id = id
        self.secret = secret

        self.callback_url = 'http://localhost:{0}/code/'.format(port)

        print("CLIENT ID: %s" % self.id)
        print("CLIENT SECRET: %s" % self.secret)
        print("Callback URL: %s" % self.callback_url)

        if auth_token == None:

            self.authentication = LinkedInAuthentication(
                self.id,
                self.secret,
                self.callback_url,

                permissions=['r_basicprofile', 'r_emailaddress', 'rw_company_admin', 'w_share']
            )

            if auth_code == None:
                print("Please open this address in your browser in order to obtain the authorization_code\n\n")
                print(self.authentication.authorization_url)

                print(
                    "\n\nIn case of error, please double check that the callback URL has been correctly added in the developer console: https://www.linkedin.com/developer/apps/")
                sys.exit()

            else:
                self.authentication.authorization_code = auth_code
                result = self.authentication.get_access_token()

                print("\n\nAccess Token:", result.access_token)
                print("Expires in (seconds):", result.expires_in)
                sys.exit()

        else:
            print
            self.application = LinkedInApplication(token=auth_token)


'''
# Deprecated Routes:

lkin_api.application.get_connections()
lkin_api.application.search_profile(selectors=[{'people': ['first-name', 'last-name']}], params={'keywords': 'apple microsoft'})
lkin_api.application.search_job(selectors=[{'jobs': ['id', 'customer-job-code', 'posting-date']}], params={'title': 'python', 'count': 2})
lkin_api.application.get_group(41001)

title = 'Scala for the Impatient'
summary = 'A new book has been published'
submitted_url = 'https://horstmann.com/scala/'
submitted_image_url = 'https://horstmann.com/scala/images/cover.png'
description = 'It is a great book for the keen beginners. Check it out!'
lkin_api.application.submit_group_post(41001, title, summary, submitted_url, submitted_image_url, description)

from linkedin.linkedin import NETWORK_UPDATES
update_types = (NETWORK_UPDATES.CONNECTION, NETWORK_UPDATES.PICTURE)
lkin_api.application.get_network_updates(update_types)

from linkedin.models import LinkedInRecipient, LinkedInInvitation
recipient = LinkedInRecipient(None, 'john.doe@python.org', 'John', 'Doe')
invitation = LinkedInInvitation('Hello John', "What's up? Can I add you as a friend?", (recipient,), 'friend')
application.send_invitation(invitation)
'''
