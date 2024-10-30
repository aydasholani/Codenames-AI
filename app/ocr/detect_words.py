import os
import numpy as np

from ..model.load_model import load_yolo_model
from ..model.detect_objects import detect_objects
from ..image_processing.save_images import save_card_images
from ..image_processing.read_image import read_image
from ..image_processing.extract_boxes import extract_boxes
from ..image_processing.sort_boxes import sort_boxes
from .text_recognition import recognize_text_from_boxes, initialize_easyocr, check_word_in_list


def detect_words(image, conf=0.5, tolerance=50):
    model_path = os.path.join(os.getcwd(), "modelv12", "runs/detect/train/weights/best.pt")
    save_dir = os.path.join(os.getcwd(), "modelv12")
    
    # Använd ett standardnamn för bilden om du behöver det för att spara resultat
    image_name = "processed_image"

    # Konvertera PIL-bild till en NumPy-array för YOLO och annan bearbetning
    img = np.array(image)

    # Ladda YOLO-modellen
    model = load_yolo_model(model_path)
    if model is None:
        return None, [], []

    # Detect objects (cards and textboxes)
    results = detect_objects(model, img, conf, save_dir)

    # Extract bounding boxes
    card_boxes, textbox_boxes = extract_boxes(results)
    if not card_boxes:
        print("No cards detected.")
        return img, card_boxes, textbox_boxes

    # Sortera kortboxar och textboxar
    sorted_card_boxes = sort_boxes(card_boxes, tolerance)
    sorted_textbox_boxes = sort_boxes(textbox_boxes, tolerance)

    # OCR på textboxarna
    reader = initialize_easyocr(lang_list=['en', 'sv'])  # Lägg till andra språk vid behov
    recognized_texts = recognize_text_from_boxes(img, sorted_textbox_boxes, reader)

    # Filtrera igenkända texter mot ordlistan
    correct_words = []
    for text in recognized_texts:
        if check_word_in_list(text):
            correct_words.append(text)
        else:
            print(f"Word '{text}' is not in the word list.")

    # Kontrollera om vi har tillräckligt många korrekt identifierade ord
    if len(correct_words) < 25:
        print("Not enough correct words detected.")
        return img, card_boxes, textbox_boxes  # Returnera om det finns för få korrekta ord

    # Spara kortbilderna och korrekt identifierade ord om tillräckligt många ord hittas
    save_card_images(img, textbox_boxes, correct_words, image_name)
    print(correct_words)

    return correct_words