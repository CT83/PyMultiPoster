# TODO Instagram uses the email and password method this should be made oauth later
from SocialMedia.SocialMedia import SocialMedia


class Instagram(SocialMedia):

    def __init__(self, e, p):
        from InstagramAPI import InstagramAPI
        self.email_address = e
        self.password = p
        self.instagrammer = InstagramAPI(self.email_address, self.password)
        self.instagrammer.login()

    def publish_update_with_image_attachment(self, message, name_att, link_att,
                                             caption_att,
                                             description_att,
                                             image_url):
        self.instagrammer.uploadPhoto(image_url, caption=message)
