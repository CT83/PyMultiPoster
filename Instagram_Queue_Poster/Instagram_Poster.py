# TODO Instagram uses the email and password method this should be made oauth later
import os
from pathlib import Path

from PIL import Image

from SocialMedia.SocialMedia import SocialMedia


class Instagram(SocialMedia):

    def __init__(self, e, p):
        from InstagramAPI import InstagramAPI
        self.email_address = e
        self.password = p
        self.instagrammer = InstagramAPI(self.email_address, self.password)
        self.converted_image = None

    def publish_update_with_image_attachment(self, message, image_url, **kwargs):
        self.instagrammer.login()
        self.instagrammer.uploadPhoto(image_url, caption=message)
        self.instagrammer.logout()

    def convert_image_to_compatible_format(self, image, compatible_format=".jpg"):
        # Convert Image to JPG
        im = Image.open(image)
        rgb_im = im.convert('RGB')

        converted_image = Path(image).stem + compatible_format
        remove_file(converted_image)
        rgb_im.save(converted_image)
        self.converted_image = converted_image
        return converted_image

    # TODO Fix this hacky method
    def convert_publish_update_with_image_attachment(self, message, image_url,
                                                     compatible_format=".jpg", **kwargs):
        im = Image.open(image_url)
        rgb_im = im.convert('RGB')

        converted_image = Path(image_url).stem + compatible_format
        remove_file(converted_image)
        rgb_im.save(converted_image)
        self.converted_image = converted_image

        self.instagrammer.login()
        self.instagrammer.uploadPhoto(converted_image, caption=message)
        self.instagrammer.logout()
        remove_file(self.converted_image)

    def cleanup(self):
        remove_file(self.converted_image)


def main():
    instagram_api = Instagram("PyMultiPoster_Bot_2", "cybertech83")
    instagram_api.convert_image_to_compatible_format('imge.jpg')
    instagram_api.publish_update_with_image_attachment("TEMP", 'imge.jpg')


def remove_file(file):
    try:
        os.remove(file)
    except OSError:
        pass


if __name__ == '__main__':
    main()

# stored_c = get_cookie(request)
# stored_c = get_credentials(get_current_user())
#
# instagram_api = Instagram(stored_c['instagram_email'],
#                           stored_c['instagram_password'])
# jpg_image = instagram_api.convert_image_to_compatible_format(image)
# Thread(target=instagram_api.convert_publish_update_with_image_attachment,
#        kwargs=dict(message=post,
#                    image_url=image)).start()

# instagram_api.cleanup()
