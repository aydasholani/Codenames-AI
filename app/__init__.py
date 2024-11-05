from flask import Flask, render_template, request

from .image_processing.read_image import load_and_preprocess_image
from .ocr.detect_words import detect_words
from .ocr.words_with_colors import create_words_with_colors
def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        detected_words = []
        error = None
        words_with_colors = []
        if request.method == 'POST':

            if 'file' not in request.files:
                error = "No file part in request"
            else:
                file = request.files['file']
                if file.filename == '':
                    error = "Ingen vald fil"
                else:
                    try:
                        image = load_and_preprocess_image(file)
                        detected_words = detect_words(image) 
                        if detected_words is None or len(detected_words) == 0:
                            error = "Hittar inte tillräckligt många ord."
                        else:
                            words_with_colors = create_words_with_colors(detected_words)
                    except Exception as e:
                        error = f"Error: {str(e)}"

        print(words_with_colors)
        return render_template('routes/index.html', detected_words=detected_words, words_with_colors=words_with_colors, error=error)


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)