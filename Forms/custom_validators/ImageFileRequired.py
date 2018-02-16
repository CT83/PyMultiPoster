import imghdr

# https://gist.github.com/msukmanowsky/8086892
from wtforms import ValidationError


class ImageFileRequired(object):
    """
    Validates that an uploaded file from a flask_wtf FileField is, in fact an
    image.  Better than checking the file extension, examines the header of
    the image using Python's built in imghdr module.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        try:
            if field.data is None or imghdr.what('unused', field.data.read()) is None:
                message = self.message or 'An image file is required'
                raise ValidationError(message)
            field.data.seek(0)
        except AttributeError as e:
            print(e)
