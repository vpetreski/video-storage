import cgi
import json
import mimetypes
import os
from pathlib import Path
from typing import Final

import requests
import typer
from requests import Response

app = typer.Typer()

API: Final = 'http://localhost/api/v1/files/'


def p_r(r: Response):
    p_s(json.dumps(r.json()))


def p_s(s: str):
    typer.secho(s, fg=typer.colors.MAGENTA, bold=True)


@app.callback()
def callback():
    """
    Video Store CLI
    """


@app.command()
def upload(path: Path = typer.Argument(..., help="Path to the video file", exists=True, file_okay=True, dir_okay=False,
                                       writable=False, readable=True, resolve_path=True)):
    """
    Upload video file from the given path
    """
    files = {'data': (path.name, open(path, 'rb'), mimetypes.types_map[os.path.splitext(path)[1]])}
    p_r(requests.post(API, files=files))


@app.command()
def delete(id: int = typer.Argument(..., help="File ID")):
    """
    Delete video file with the given id
    """
    p_r(requests.delete(API + str(id)))


@app.command()
def download(id: int = typer.Argument(..., help="File ID")):
    """
    Download video file from the given id to the current directory
    """
    response = requests.get(API + str(id))
    if response.status_code == 200:
        file_name = cgi.parse_header(response.headers['Content-Disposition'])[1]['filename']
        with open(file_name, 'wb') as f:
            f.write(response.content)
        p_s(f"File {file_name} saved!")
    else:
        p_r(response)


@app.command()
def list():
    """
    List all video files
    """
    p_r(requests.get(API))
