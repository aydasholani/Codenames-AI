from PIL import Image
from flask import Flask, jsonify, render_template, request, url_for
from PIL import Image
from .ocr.detect_words import detect_words
from .ocr.words_with_colors import create_words_with_colors
def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        detected_words = []  # Tom lista för de detekterade orden
        error = None  # Variabel för felmeddelanden
        words_with_colors = []
        if request.method == 'POST':
            # Kontrollera om en fil skickades med förfrågan
            if 'file' not in request.files:
                error = "No file part in request"
            else:
                file = request.files['file']
                if file.filename == '':
                    error = "No selected file"
                else:
                    try:
                        # Läs in bilden och bearbeta den
                        image = Image.open(file.stream)
                        detected_words = detect_words(image)  # Kör ordigenkänningsfunktionen
                        if detected_words:
                            words_with_colors = create_words_with_colors(detected_words)
                    except Exception as e:
                        error = f"Error processing image: {str(e)}"

        print(words_with_colors)
        return render_template('routes/index.html', detected_words=detected_words, words_with_colors=words_with_colors, error=error)


    return app
# Om skriptet körs direkt, skapa och kör appen
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)