import io

from minio import Minio
from dotenv import load_dotenv
from minio.error import MinioException

load_dotenv()

ACCESS_KEY = 'testserver_user'
SECRET_KEY = 'testserver_pass'
MINIO_API_HOST = '45.141.101.148:9000'


class MinIO:
    def __init__(self):
        self.minio_client = Minio(MINIO_API_HOST, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

    def upload_image(self, bucket_name, filename, image):
        try:
            if not self.minio_client.bucket_exists(bucket_name):
                self.minio_client.make_bucket(bucket_name)
            self.minio_client.put_object(bucket_name, filename, io.BytesIO(image), length=len(image))
        except MinioException:
            print("MinIO: Error while uploading data")

    def delete_image(self, bucket_name, filename):
        try:
            self.minio_client.remove_object(bucket_name, filename)
        except MinioException:
            print("MinIO: Error while deleting data")
