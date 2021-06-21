import uuid
import boto3

from flask import current_app

class S3Service:
    @staticmethod
    def upload(file, bucket_name=None, acl='public-read', path=''):
        return S3Uploader.upload(file=file, bucket_name=bucket_name, acl=acl, path=path)

    @staticmethod
    def read(bucket_name, key):
        return S3Reader.read(bucket_name=bucket_name, key=key)


class S3Reader:
    @staticmethod
    def read(key, bucket_name):
        ACCESS_KEY = current_app.config.get('AWS_ACCESS_KEY_ID')
        SECRET_KEY = current_app.config.get('AWS_SECRET_ACCESS_KEY')

        client = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,)
        try:
            obj = client.get_object(
                Bucket=bucket_name,
                Key=key
            )
        except:
            return False

        try:
            return obj
        except:
            pass

        return None

class S3Uploader:
    @staticmethod
    def upload(file, bucket_name=None, acl='public-read', path=''):
        ACCESS_KEY = current_app.config.get('AWS_ACCESS_KEY_ID')
        SECRET_KEY = current_app.config.get('AWS_SECRET_ACCESS_KEY')
        BUCKET_NAME = bucket_name or current_app.config.get('DEFAULT_AWS_BUCKET_NAME')
        print(file)
        path = '{}/'.format(path) if path else ''
        key = '{}{}'.format(path, S3Uploader.__generate_name(file))
        client = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY)
        client.put_object(
            ACL=acl,
            Bucket=BUCKET_NAME,
            Key=key,
            Body=file,

            ContentType=file.mimetype)
        return {
            'url': "https://{}.s3.amazonaws.com/{}".format(
                BUCKET_NAME, key),
            'acl': acl,
            'bucket_name': bucket_name,
            'path': path,
            'key': key
        }
    @staticmethod
    def __generate_name(file):
        extension = file.filename.split('.')[-1]

        return '{}.{}'.format(uuid.uuid4().hex, extension)
