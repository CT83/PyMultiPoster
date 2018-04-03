import boto3

from CONSTANT import S3_BUCKET, S3_SECRET, S3_KEY


class S3:
    def __init__(self, bucket, key, secret):
        self.bucket = bucket
        self.key = key
        self.secret = secret
        self.location = "https://s3.amazonaws.com/{}".format(bucket)

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret
        )

    def upload(self, source_file, destination_filename=None):

        if destination_filename is None:
            destination_filename = source_file.name

        try:

            self.s3.upload_fileobj(
                source_file,
                self.bucket,
                destination_filename,
                ExtraArgs={'ACL': 'public-read'})

        except Exception as e:
            print("AWS Upload Error : ", e)
            return e

        return "{}/{}".format(self.location, destination_filename)


if __name__ == '__main__':
    s3 = S3(bucket=S3_BUCKET,
            key=S3_KEY,
            secret=S3_SECRET)
    file = open('21tread.txt', 'rb')
    print(s3.upload(file))
