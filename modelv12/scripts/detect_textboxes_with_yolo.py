import os
from model.load_model import load_yolo_model
from model.detect_objects import detect_objects
from image_processing.save_images import save_card_images
from image_processing.read_image import read_image
from image_processing.extract_boxes import extract_boxes
from image_processing.sort_boxes import sort_boxes
from ocr.text_recognition import recognize_text_from_boxes, initialize_easyocr


def detect_words_with_yolo(image_path, conf=0.5, tolerance=50):
    model_path = os.path.join(os.getcwd(), "modelv12", "runs/detect/train/weights/best.pt")
    save_dir = os.path.join(os.getcwd(), "modelv12")
    
    
    image_name = os.path.basename(image_path).split(".")[0]
    # Load the YOLO model
    model = load_yolo_model(model_path)
    if model is None:
        return None, [], []

    # Read the image
    img = read_image(image_path)
    if img is None:
        return None, [], []

    # Detect objects (cards and textboxes)
    results = detect_objects(model, img, conf, save_dir)

    # Extract bounding boxes
    card_boxes, textbox_boxes = extract_boxes(results)
    if not card_boxes:
        print("No cards detected.")
        return img, card_boxes, textbox_boxes

    # Sort card boxes by position and save them
    sorted_card_boxes = sort_boxes(card_boxes, tolerance)

    reader = initialize_easyocr(lang_list=['en', 'sv'])  # Lägg till andra språk vid behov
    recognized_texts = recognize_text_from_boxes(img, textbox_boxes, reader)
    save_card_images(img, sorted_card_boxes, recognized_texts, image_name)

    return recognized_texts


test_image = os.path.join(os.getcwd(), "modelv12", "test", "board_003.png")
detect_words_with_yolo(test_image)



folder = os.path.join(os.getcwd(), "modelv12", "test")

for img in os.listdir(folder):
    img_path = os.path.join(folder, img)
    if img_path.endswith((".png", ".jpg", ".jpeg")):

        texts = detect_words_with_yolo(img_path)
        print(texts)
        print(len(texts)/25)
        print(type(texts))
