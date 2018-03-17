import os

import boto3

S3_BUCKET = "pymultiposter-2"
S3_KEY = "AKIAJEYHDBZNM4XQTOHA"
S3_SECRET = "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"
# S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
S3_LOCATION = "https://s3.amazonaws.com/{}".format(S3_BUCKET)

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name):
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.name)

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(S3_LOCATION, file.name)


f = open("read.txt", "w+")
for i in range(10):
    f.write("This is line %d\r\n" % (i + 1))
f = open('read.txt', 'rb')
upload_file_to_s3(f, S3_BUCKET)
