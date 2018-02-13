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
        self.instagrammer.login()
        self.converted_image = None

    def publish_update_with_image_attachment(self, message, image_url):
        self.instagrammer.uploadPhoto(image_url, caption=message)

    def convert_image_to_compatible_format(self, image, compatible_format=".jpg"):
        # Convert Image to JPG
        im = Image.open(image)
        rgb_im = im.convert('RGB')
        remove_file(image)

        converted_image = Path(image).stem + compatible_format
        remove_file(converted_image)
        rgb_im.save(converted_image)
        self.converted_image = converted_image
        return converted_image

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
