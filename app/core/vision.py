"""
Contains object detection module
using a pre-trained Faster R-CNN model from PyTorch.
"""

from torchvision import models
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights

# The human-readable labels for each class index
COCO_CATEGORIES = FasterRCNN_ResNet50_FPN_Weights.DEFAULT.meta["categories"]

# Load the pre-trained Faster R-CNN model with ResNet-50 backbone
model = models.detection.fasterrcnn_resnet50_fpn(
    weights=FasterRCNN_ResNet50_FPN_Weights.COCO_V1
)

# Set the model to evaluation mode
model.eval()
