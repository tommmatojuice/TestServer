import io

from minio import Minio
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = 'admin1'
SECRET_KEY = 'password1'
MINIO_API_HOST = "localhost:9000"


class MinIO:
    def __init__(self):
        self.minio_client = Minio(MINIO_API_HOST, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

    def upload_image(self, bucket_name, filename, image):
        if not self.minio_client.bucket_exists(bucket_name):
            print(f'create a bucket {bucket_name}')
            self.minio_client.make_bucket(bucket_name)
        else:
            print("Bucket already exists")
        try:
            self.minio_client.put_object(bucket_name, filename, io.BytesIO(image), length=len(image))
        except Exception:
            print("error")
