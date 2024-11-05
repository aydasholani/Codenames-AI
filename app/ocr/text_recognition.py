import easyocr
import os
from difflib import get_close_matches
from fuzzywuzzy import fuzz
from spellchecker import SpellChecker

def load_word_list():
    """Load the word list from a file."""
    file_path = os.path.join(os.getcwd(), "app", "ocr", 'codenames-swedish.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        word_list = {line.strip().upper() for line in file} 
    return word_list
  
def check_word_in_list(word):
    """Check if the cleaned text matches any word in the word list, or suggest closest match."""
    word_list = load_word_list()

    if word in word_list:
        print("Exakt matchning hittades: ", word)
        return word
 
    close_matches = get_close_matches(word, word_list, n=1, cutoff=0.6)  

    best_match = close_matches[0].upper() if close_matches else None
    print(f"Original word: {word}, Suggested match: {best_match}")
    return best_match

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
            min_size=4
    )
    
    for (bbox, text, prob) in results:
        print(f'Text: {text}, Probability: {prob}')
    return results

def recognize_text(image, boxes, min_words=25):
    """Recognizes text in each specified bounding box in the image, filters recognized words, and checks for minimum word count."""
    correct_words = []
    reader = initialize_easyocr()  # Initialisera OCR-läsaren en gång
    
    for (x1, y1, x2, y2) in boxes:
        # Beskär textboxen
        textbox = image[y1:y2, x1:x2]
        
        # Kör OCR på det beskurna textområdet
        results = read_text_from_textbox(reader, textbox)
        # Extrahera och filtrera text
        for text in results:
            recognized_text = text[1].strip().upper()  
            corrected_word = check_word_in_list(recognized_text)
    
            # Lägg till det korrigerade ordet om det finns en matchning
            if corrected_word:
                correct_words.append(corrected_word)
            else:
                correct_words.append("Null") 
                

    return correct_words