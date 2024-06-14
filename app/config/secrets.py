"""
Contains the project configurations
and environment variables.
"""

import os

from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

DEBUG = os.environ.get("DEBUG", "False") == "True"

# Load environment variables from .env
load_dotenv(Path(BASE_DIR).joinpath(".env"))

file_formats = os.environ.get("ACCEPT_FILE_FORMATS", None)

if not file_formats:
    ACCEPT_FILE_FORMATS = ["mp4"]
else:
    ACCEPT_FILE_FORMATS = file_formats.split(";")

VIDEO_DURATION_LIMIT = int(os.environ.get("VIDEO_DURATION_LIMIT", "300"))

FRAME_CAPTURE_INTERVAL = int(os.environ.get("FRAME_CAPTURE_INTERVAL", "4"))

CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", 0.75))

if CONFIDENCE_THRESHOLD <= 0:
    CONFIDENCE_THRESHOLD = 0.1

if CONFIDENCE_THRESHOLD > 1:
    CONFIDENCE_THRESHOLD = 1
