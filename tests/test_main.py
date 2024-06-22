"""
Contains a test case for /vision.
"""

# mypy: ignore-errors

import os

from fastapi.testclient import TestClient
from moviepy import ColorClip

from app.main import app


client = TestClient(app)


def test_invalid_content_type():
    response = client.post(
        "/vision",
        files={
            "file": ("example.mp3", "example.mp3", "audio/mp3"),
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid content type"}


def test_too_long_video():
    pathname = "test.mp4"

    video = ColorClip(size=(256, 256), color=(0, 0, 0), duration=1000)
    video.write_videofile(pathname, fps=24)

    with open(pathname, "rb") as f:
        response = client.post(
            "/vision",
            files={
                "file": (pathname, f, "video/mp4"),
            },
        )
    assert response.status_code == 400

    body = response.json()

    assert "detail" in body and body["detail"].startswith("Too long")

    video.close()
    os.remove(pathname)


def test_successful_request():
    pathname = "test.mp4"

    video = ColorClip(size=(256, 256), color=(0, 0, 0), duration=4)
    video.write_videofile(pathname, fps=24)

    with open(pathname, "rb") as f:
        response = client.post(
            "/vision",
            files={
                "file": (pathname, f, "video/mp4"),
            },
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"

    video.close()
    os.remove(pathname)
