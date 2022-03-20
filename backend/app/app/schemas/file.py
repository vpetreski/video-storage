from datetime import datetime

from pydantic import BaseModel


class UploadedFile(BaseModel):
    id: int = None
    name: str
    size: int
    created_at: datetime

    class Config:
        orm_mode = True
