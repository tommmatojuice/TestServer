from datetime import datetime
from pydantic import BaseModel


class Image:
    def __init__(self, image_id, request_code, file_name, reg_date):
        self.image_id = image_id
        self.request_code = request_code
        self.file_name = file_name
        self.reg_date = reg_date


class ImageOut(BaseModel):
    request_code: str
    file_name: str
    reg_date: datetime
