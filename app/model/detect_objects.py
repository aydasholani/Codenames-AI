
def detect_objects(model, img, conf, save_dir):
    """Runs the YOLO model prediction on the image and returns results."""
    return model.predict(
        img,
        conf=conf,
        imgsz=640,
        save=False,
        project="modelv12",
        name="runs/detect/test"
    )