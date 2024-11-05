import os
import numpy as np

from ..model.load_model import load_yolo_model
from ..model.detect_objects import detect_objects
from ..image_processing.extract_boxes import extract_boxes
from ..image_processing.sort_boxes import sort_boxes
from .text_recognition import recognize_text, initialize_easyocr, check_word_in_list


def detect_words(image, conf=0.5, tolerance=50):
    model_path = os.path.join(os.getcwd(), "app", "model", "best.pt")

    # Konvertera PIL-bild till en NumPy-array för YOLO och annan bearbetning
    img = np.array(image)

    # Ladda YOLO-modellen
    model = load_yolo_model(model_path)
    if model is None:
        return None, [], []

    # Detect objects (cards and textboxes)
    results = detect_objects(model, img, conf)

    # Extract bounding boxes
    card_boxes, textbox_boxes = extract_boxes(results)
    if not card_boxes:
        print("No cards detected.")
        return img, card_boxes, textbox_boxes

    # Sortera textboxar
    sorted_textboxes = sort_boxes(textbox_boxes, tolerance)


    correct_words = recognize_text(img, sorted_textboxes)

    return correct_words