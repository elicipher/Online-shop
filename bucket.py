import boto3
from django.conf import settings
import logging 
from botocore.exceptions import ClientError
import os

class Bucket:
    '''CDN bucket manager

        init method create connection.

        NOTE: none of these method are async. use public interface in tasks.py in moduls instead.
    '''
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        try:
            self.s3_resource = boto3.client(
            service_name= settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        except Exception as exc:
            logging.info(exc)
            self.s3_resource = None  # اگر اتصال موفق نبود، None قرار بده
    
    def get_objects(self):
            if not self.s3_resource :
                logging.error("S3 resource is not initialized.")
                return  
            try:
               result = self.s3_resource.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
               if result['KeyCount'] : # اگر کلیدها وجود داشتند
                   result = result['Contents'] 
                   return result
               else:
                   return None
               
            except ClientError as exc:
                logging.error(exc)

    def delete_object(self , key):
        self.s3_resource.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME , Key = key)
        return True
    
    def download_object(self, key):
        local_path = os.path.join(settings.AWS_LOCAL_STORAGE, key)

        # دایرکتوری‌های میانی رو بساز
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        with open(local_path, 'wb') as data:
            self.s3_resource.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key,data)

    
    def upload_object(self , key):

        with open(key, 'rb') as data:
            self.s3_resource.upload_fileobj(data, settings.AWS_STORAGE_BUCKET_NAME, key)
        
             
        


            


bucket = Bucket()
