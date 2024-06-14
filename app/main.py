"""
Entry point to the service.
"""

import csv
import io
import math
import os
import tempfile

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from moviepy import VideoFileClip

from app.config.secrets import (
    ACCEPT_FILE_FORMATS,
    VIDEO_DURATION_LIMIT,
    FRAME_CAPTURE_INTERVAL,
)
from app.utils.logger import logger
from app.core.vision import process_frame

app = FastAPI(
    title="Objects on video detection API",
    version="0.1.0",
    description="Detectes objects on a given video using PyTorch",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/vision")
async def process(
    file: UploadFile = File(...),
) -> StreamingResponse:
    # Content type validation
    if not file.content_type.startswith("video/"):  # type: ignore[union-attr]
        raise HTTPException(status_code=400, detail="Invalid content type")

    # Validate file format
    file_format = file.filename.split(".")[-1]  # type: ignore[union-attr]

    if file_format not in ACCEPT_FILE_FORMATS:
        detail = f"Supported files: {", ".join(ACCEPT_FILE_FORMATS)}"
        raise HTTPException(status_code=400, detail=detail)

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=file.filename.lower()  # type: ignore[union-attr]
    ) as temp:
        temp.write(await file.read())
        pathname = temp.name

    video = VideoFileClip(pathname)

    if video.duration > VIDEO_DURATION_LIMIT:
        raise HTTPException(
            status_code=400,
            detail=f"Too long. Limit is {VIDEO_DURATION_LIMIT} seconds",
        )

    logger.info("The vide0 file is valid, starting AI processing...")

    results = []

    for t in range(0, int(math.floor(video.duration)), FRAME_CAPTURE_INTERVAL):
        predictions = process_frame(video, t)
        results.extend(predictions)

    logger.info("The video has been processed! Creating CSV...")

    # Close the video file
    # and remove it from a temp storage
    video.close()
    os.remove(pathname)

    # Write to csv
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "timestamp",
            "label",
            "score",
            "x_min",
            "y_min",
            "x_max",
            "y_max",
        ],
    )
    writer.writeheader()
    writer.writerows(results)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=results.csv"},
    )
