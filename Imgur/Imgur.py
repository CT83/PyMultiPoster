import pyimgur

from CONSTANT import IMGUR_CLIENT_ID


def upload_to_imgur(client, path):
    im = pyimgur.Imgur(client)
    uploaded_image = im.upload_image(path, title="Uploaded by PyMuliPoster")
    # print(uploaded_image.title)
    # print(uploaded_image.link)
    # print(uploaded_image.size)
    # print(uploaded_image.type)
    return uploaded_image.link


upload_to_imgur(IMGUR_CLIENT_ID, 'temp.jpg')
