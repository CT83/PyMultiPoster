# TODO In future add getUserInfo Methods here to retrieve friends list and profile info


class SocialMedia:
    def get_authorization_url(self):
        pass

    def get_oauth_token(self, authorization_code):
        pass

    def publish_update(self, message, **kwargs):
        pass

    def publish_update_image(self, message, image):
        pass

    def publish_update_with_attachment(self, **kwargs):
        pass

    def publish_update_with_image_attachment(self, message, image_url, **kwargs):
        pass

    def get_user_id_name(self):
        pass

    def get_profile_name(self):
        pass
