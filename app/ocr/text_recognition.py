import easyocr
import os

def load_word_list():
    """Load the word list from a file."""
    file_path = os.path.join(os.getcwd(), "modelv12", 'codenames-swedish.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        word_list = {line.strip().upper() for line in file} 
    return word_list
  
def check_word_in_list(word):
    """Check if the cleaned text matches any word in the word list."""
    word_list = load_word_list()
    return word.upper() in word_list

def initialize_easyocr(lang_list=['en']):
    """Initializes the EasyOCR reader."""
    return easyocr.Reader(["sv"], gpu=True)
  
  
def recognize_text_from_boxes(image, boxes, reader):
    """Recognizes text in each specified bounding box in the image."""
    text_results = []
    word_list = load_word_list()
    for (x1, y1, x2, y2) in boxes:
        
        # Beskär textboxen
        textbox_img = image[y1:y2, x1:x2]
        
        # Kör OCR på det beskurna textområdet
        results = reader.readtext(textbox_img, decoder='wordbeamsearch', beamWidth=10)
        
        # Extrahera text från OCR-resultat
        detected_text = " ".join([text[1] for text in results])
        text_results.append(detected_text)
        
    return text_results