"""
Contains object detection module
using a pre-trained Faster R-CNN model from PyTorch.
"""

from typing import Any, List, Union

import torch

from moviepy import VideoFileClip
from torchvision import models
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
from torchvision.transforms.functional import to_tensor
from PIL import Image

from app.config.secrets import CONFIDENCE_THRESHOLD

# The human-readable labels for each class index
COCO_CATEGORIES = FasterRCNN_ResNet50_FPN_Weights.DEFAULT.meta["categories"]

# Load the pre-trained Faster R-CNN model with ResNet-50 backbone
model = models.detection.fasterrcnn_resnet50_fpn(
    weights=FasterRCNN_ResNet50_FPN_Weights.COCO_V1
)

# Set the model to evaluation mode
model.eval()


def process_frame(
    video: VideoFileClip,
    timestamp: Union[int, float],
) -> List[dict[str, Any]]:
    """
    Detects objects in a given video at a given time using
    a pre-trained PyTorch model.

    Args:
        video (VideoFileClip): A video object
        timestamp (int | float): The timestamp in seconds.

    Returns:
        A list of detected objects, where each object contains
        the following fields:
            - label: a COCO category
            - score: confidence score
            - x_min, y_min, x_max, y_max: Bounding box coordinates
    """

    image = video.get_frame(timestamp)
    image = Image.fromarray(image)

    # Convert the PIL image to a tensor
    tensor = to_tensor(image)

    # Perform inference without tracking gradients
    with torch.no_grad():
        preds = model([tensor])[0]

    image.close()

    # Extract, format, and return predictions
    results = [
        {
            "timestamp": timestamp,
            "label": COCO_CATEGORIES[label.item()],
            "score": round(score.item(), 2),
            "x_min": round(box[0].item(), 2),
            "y_min": round(box[1].item(), 2),
            "x_max": round(box[2].item(), 2),
            "y_max": round(box[3].item(), 2),
        }
        for label, score, box in zip(
            preds["labels"],
            preds["scores"],
            preds["boxes"],
        )
        if score >= CONFIDENCE_THRESHOLD
    ]

    return results
