import os
from io import BytesIO
from snitch.config import config
from tests.utils import send_json, app


def test_upload(app):
    data = dict(file=(BytesIO(b'4815162342'), "4815162342.jpg.real_ext"))
    response = app.post("/upload", content_type='multipart/form-data', data=data)
    assert response.status_code == 400

    data = dict(file=(BytesIO(b'4815162342'), "4815162342.jpg"))
    response = app.post("/upload", content_type='multipart/form-data', data=data)
    assert response.status_code == 201
    assert "filename" in response.get_json()
    assert os.path.exists(os.path.join(config.UPLOAD_FOLDER, response.get_json()["filename"]))
    os.remove(os.path.join(config.UPLOAD_FOLDER, response.get_json()["filename"]))


def test_download(app):
    filename = "ee2a6403-6420-49e6-893a-4effdc34f860.jpg"
    with open(os.path.join(config.UPLOAD_FOLDER, filename), "wb") as image:
        image.write(b"4815162342")

    response = send_json(app, "get", "/upload", dict(filename=filename))
    assert response.status_code == 200
    assert response.data == b"4815162342"
    os.remove(os.path.join(config.UPLOAD_FOLDER, filename))
