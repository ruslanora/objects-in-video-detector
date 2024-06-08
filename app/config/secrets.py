"""
Contains the project secrets.
"""

import os

from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

DEBUG = os.environ.get("DEBUG", "False") == "True"

# Load environment variables from .env
load_dotenv(Path(BASE_DIR).joinpath(".env"))
