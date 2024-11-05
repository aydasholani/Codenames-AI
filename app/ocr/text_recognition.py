import easyocr
import os
from difflib import get_close_matches

def load_word_list():
    file_path = os.path.join(os.getcwd(), "app", "ocr", 'codenames-swe.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        word_list = {line.strip().upper() for line in file} 
    return word_list
  
def check_word_in_list(word):
    word_list = load_word_list()

    if word in word_list:
        print("Exakt matchning hittades: ", word)
        return word
 
    close_matches = get_close_matches(word, word_list, n=1, cutoff=0.6)  

    best_match = close_matches[0].upper() if close_matches else None
    print(f"Original word: {word}, Suggested match: {best_match}")
    return best_match

def initialize_easyocr(lang_list=['sv', 'en']):
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
    correct_words = []
    reader = initialize_easyocr()
    
    for (x1, y1, x2, y2) in boxes:

        textbox = image[y1:y2, x1:x2]

        results = read_text_from_textbox(reader, textbox)

        for text in results:
            recognized_text = text[1].strip().upper()  
            corrected_word = check_word_in_list(recognized_text)

            if corrected_word:
                correct_words.append(corrected_word)
            else:
                correct_words.append("Null") 
                

    return correct_words