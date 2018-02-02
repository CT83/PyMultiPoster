# TODO In future add getUserInfo Methods here to retrieve friends list and profile info


class SocialMedia:
    def get_authorization_url(self):
        pass

    def get_oauth_token(self, authorization_code):
        pass

    def publish_update(self, message):
        pass

    def publish_update_with_attachment(self, message, name_att, link_att, caption_att, description_att):
        pass

    def publish_update_with_image_attachment(self, message, name_att, link_att,
                                             caption_att,
                                             description_att,
                                             image_url):
        pass
