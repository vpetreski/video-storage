import glob
import os

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.file import File


def test_videos(client: TestClient, db: Session) -> None:
    # Clean slate
    files = glob.glob('videos/*')
    for f in files:
        os.remove(f)
    try:
        db.query(File).delete()
        db.commit()
    except:
        db.rollback()

    video_file_name: str = "video1.mp4"

    # Upload
    response = client.post(
        f"{settings.API_V1_STR}/files/",
        files={"data": (video_file_name, open(f'app/tests/data/{video_file_name}', "rb"), "video/mp4")}
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == video_file_name
    assert "id" in content
    assert "size" in content
    assert "created_at" in content

    # List
    response = client.get(
        f"{settings.API_V1_STR}/files/"
    )
    assert response.status_code == 200
    content = response.json()
    assert content[0]["name"] == video_file_name

    # Delete
    response = client.delete(
        f"{settings.API_V1_STR}/files/{content[0]['id']}"
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == video_file_name
