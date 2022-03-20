import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Set, List, Any

from fastapi import APIRouter, UploadFile, Request, Response, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, crud
from app.api import deps

router = APIRouter()

videos_path: str = 'videos/'
Path(videos_path).mkdir(parents=True, exist_ok=True)

supported_content_types: Set[str] = {'video/mp4', 'video/mpeg'}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UploadedFile,
             responses={status.HTTP_201_CREATED: {"description": "File uploaded"},
                        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
                        status.HTTP_409_CONFLICT: {"description": "File exists"},
                        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"description": "Unsupported Media Type"}})
def upload_video(data: UploadFile, request: Request, response: Response, db: Session = Depends(deps.get_db)) -> Any:
    """
    Upload video.
    """
    full_path: str = videos_path + data.filename

    if data.content_type not in supported_content_types:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported Media Type")

    if os.path.isfile(full_path):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File exists")

    with open(full_path, "wb") as buffer:
        shutil.copyfileobj(data.file, buffer)

    uploaded_file = schemas.UploadedFile(name=data.filename, size=os.path.getsize(full_path), created_at=datetime.now())
    file = crud.file.create(db=db, obj_in=uploaded_file)

    response.headers["Location"] = str(request.url) + str(file.id)

    return file


@router.get("/", response_model=List[schemas.UploadedFile])
def list_uploaded_videos(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve uploaded videos.
    """
    files = crud.file.get_multi(db, skip=skip, limit=limit)
    return files


@router.get("/{id}", response_class=FileResponse,
            responses={status.HTTP_200_OK: {"description": "OK", "content": {"video/mp4": {}, "video/mpeg": {}}},
                       status.HTTP_404_NOT_FOUND: {"description": "File not found"}})
async def download_video(*, db: Session = Depends(deps.get_db), id: int):
    """
    Download video by ID.
    """
    file = crud.file.get(db=db, id=id)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")

    return FileResponse(path=videos_path + file.name, filename=file.name, media_type='application/octet-stream',
                        headers={'content-disposition': f'attachment; filename="{file.name}"'},
                        status_code=status.HTTP_200_OK)


@router.delete("/{id}", response_model=schemas.UploadedFile, status_code=status.HTTP_200_OK,
               responses={status.HTTP_200_OK: {"description": "File was successfully removed"},
                          status.HTTP_404_NOT_FOUND: {"description": "File not found"}})
def delete_video(*, db: Session = Depends(deps.get_db), id: int):
    """
    Delete a video.
    """
    file_db = crud.file.get(db=db, id=id)
    if not file_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")

    os.remove(videos_path + file_db.name)
    file_db = crud.file.remove(db=db, id=id)

    return file_db
