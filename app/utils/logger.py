"""
Contains logging configuration.
"""

import logging

from app.config.secrets import DEBUG

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

handler.setFormatter(formatter)
logger.addHandler(handler)
