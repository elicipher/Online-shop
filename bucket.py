import boto3
from django.conf import settings
import logging 

class Bucket:
    '''CDN bucket manager

        init method create connection.
    '''
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        try:
            s3_resource = boto3.resource(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        except Exception as exc:
            logging.info(exc)


