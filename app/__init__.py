import os
from PIL import Image
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from flask import request
from .ocr.detect_words import detect_words
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Läs in bilden direkt i minnet
        image = Image.open(file.stream)

        # Kör detektering och OCR direkt på bilden
        detected_words = detect_words(image)

        # Returnera resultat som JSON
        return jsonify({'detected_words': detected_words})

if __name__ == '__main__':
    app.run(debug=True)