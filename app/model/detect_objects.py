import numpy as np

def detect_objects(model, img, conf):
    """Runs the YOLO model prediction on the image and returns results."""
    return model.predict(
        img,
        conf=conf,
        imgsz=640,
        save=False,
        max_det=50,
    )