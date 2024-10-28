import os
import cv2
from ultralytics import YOLO

def load_yolo_model(model_path):
    """Loads the YOLO model from a specified path."""
    if not os.path.exists(model_path):
        print(f"Model not found at: {model_path}")
        return None
    return YOLO(model_path)






