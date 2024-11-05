import easyocr
import os
import difflib

def load_word_list():
    """Load the word list from a file."""
    file_path = os.path.join(os.getcwd(), "app", "ocr", 'codenames-swe-eng.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        word_list = {line.strip().upper() for line in file} 
    return word_list
  
def check_word_in_list(word):
    """Check if the cleaned text matches any word in the word list."""
    word_list = load_word_list()
    return word.upper() in word_list

def initialize_easyocr(lang_list=['sv', 'en']):
    """Initializes the EasyOCR reader."""

    return easyocr.Reader(lang_list, gpu=True)
def read_text_from_textbox(reader, textbox):
    allowlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖabcdefghijklmnopqrstuvwxyzåäö'
    
    results = reader.readtext(
            textbox, 
            decoder='wordbeamsearch', 
            beamWidth=20, 
            allowlist=allowlist,
            min_size=5
    )
    
    for (bbox, text, prob) in results:
        print(f'Text: {text}, Probability: {prob}')
    return results

def recognize_text(image, boxes, min_words=25):
    """Recognizes text in each specified bounding box in the image, filters recognized words, and checks for minimum word count."""
    correct_words = []
 
    reader = initialize_easyocr()
    for (x1, y1, x2, y2) in boxes:
        # Beskär textboxen
        textbox = image[y1:y2, x1:x2]
        
        # Kör OCR på det beskurna textområdet
        results = read_text_from_textbox(reader, textbox)
        
        # Extrahera och filtrera text
        for text in results:
            recognized_text = text[1].strip()  # Extrahera och trimma
            if recognized_text and check_word_in_list(recognized_text):  # Kontrollera ordlistan
                correct_words.append(recognized_text.upper())  # Lägg till ordet om det är giltigt
                
    # Kontrollera om vi har tillräckligt många korrekta ord
    if len(correct_words) < min_words:
        print(f"För få korrekta ord. Endast {len(correct_words)} identifierade.")
        return []  # Returnera tom lista om vi inte har tillräckligt många korrekta ord

    return correct_words