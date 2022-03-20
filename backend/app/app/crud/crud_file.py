from app.crud.base import CRUDBase
from app.models.file import File
from app.schemas.file import UploadedFile


class CRUDFile(CRUDBase[File, UploadedFile, UploadedFile]):
    pass


file = CRUDFile(File)
