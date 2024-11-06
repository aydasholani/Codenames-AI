import os
import numpy as np

from ..model.load_model import load_yolo_model
from ..model.detect_objects import detect_objects
from ..image_processing.extract_boxes import extract_boxes
from ..image_processing.sort_boxes import sort_boxes
from .text_recognition import recognize_text


def detect_words(image, conf=0.5, tolerance=50):
    model_path = os.path.join(os.getcwd(), "app", "model", "best.pt")

    img = np.array(image)


    model = load_yolo_model(model_path)
    if model is None:
        return None, [], []


    results = detect_objects(model, img, conf)


    card_boxes, textbox_boxes = extract_boxes(results)
    if not card_boxes:
        print("No cards detected.")
        return img, card_boxes, textbox_boxes

    sorted_textboxes = sort_boxes(textbox_boxes, tolerance)


    correct_words = recognize_text(img, sorted_textboxes)

    return correct_words