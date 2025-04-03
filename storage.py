from io import BytesIO

import boto3
from botocore.client import Config
import os
from dotenv import load_dotenv

load_dotenv()
session = boto3.session.Session()


class ObjectStorage:
    def __init__(self):
        try:
            self.client = session.client(
                's3',
                endpoint_url=os.getenv('S3_ENDPOINT_URL'),
                aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
                aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
                region_name=os.getenv('S3_REGION'),
                config=Config(signature_version='s3v4')
            )
            self.bucket = os.getenv('S3_BUCKET_NAME')
            self.client.head_bucket(Bucket=os.getenv('S3_BUCKET_NAME'))
            print('Ok initializ')
        except Exception as e:
            print(f'No ok {e}')

    async def upload_file(self, file: BytesIO, object_name: str):
        """Загрузка файла в Object Storage"""
        file.seek(0)
        self.client.upload_fileobj(file, self.bucket, object_name)

        return f"https://{self.bucket}.storage.yandexcloud.net/pickup/test/{object_name}"

    async def delete_file(self, object_name: str):
        """Удаление файла"""
        self.client.delete_object(Bucket=self.bucket, Key=object_name)

    async def test_connection(self):

        try:
            r = self.client.list_buckets()
            print(f'Доступные бакеты: {[b['Name'] for b in r['Buckets']]}')
            print('Конект ок')
            return True
        except Exception as e:
            raise Exception(f'Нет соединенения{str(e)}')


# s = session.client(
#     service_name='s3',
#     endpoint_url='https://storage.yandexcloud.net'
# )
# for k in s.list_objects(Bucket='new-buket')['Contents']:
#     print(k['key'])


