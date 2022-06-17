import datetime
import uuid
from typing import List

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException

from image import Image, ImageOut
from minio_connection import MinIO
from src.db_connection import AppDb

app = FastAPI()
db = AppDb()
min_io = MinIO()
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


@app.post("/frames/", response_model=List[ImageOut])
async def upload_images(files: List[UploadFile] = File(...)):
    try:
        request_code = uuid.uuid4()
        for img in files:
            now_time = datetime.datetime.now()
            bucket_name = f'{now_time.year}{now_time.month}{now_time.day}'
            contents = await img.read()
            file_name = f"{uuid.uuid4()}.jpeg"

            min_io.upload_image(bucket_name, file_name, contents)
            db.insert_image(Image(None, request_code, file_name, now_time.strftime(TIME_FORMAT)))

        reply = [Image(img[0], img[1], img[2], img[3].strftime(TIME_FORMAT)).__dict__
                 for img in db.get_images(request_code)]

    except HTTPException:
        return {'message': 'There was an error uploading the file(s)'}

    return reply


@app.get("/frames/{request_code}", response_model=List[ImageOut])
async def read_images(request_code: str):
    try:
        return [Image(img[0], img[1], img[2].strftime(TIME_FORMAT)).__dict__
                for img in db.get_images(request_code)]

    except HTTPException:
        return {'message': 'There was an error reading the file(s)'}


@app.delete("/frames/{request_code}")
async def delete_images(request_code: str):
    try:
        images_to_delete = [Image(img[0], img[1], img[2].strftime(TIME_FORMAT)).__dict__
                            for img in db.get_images(request_code)]

        db.delete_images(request_code)

    except HTTPException:
        return {'message': 'There was an error deleting the file(s)'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
