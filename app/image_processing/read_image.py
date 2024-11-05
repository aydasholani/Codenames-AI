import cv2
import numpy as np
from PIL import Image
def read_image(image_path):
    """Reads an image from the specified path."""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        print("Filen är inte en giltig bild eller kunde inte läsas in.")
    else:
        print("Bilden är giltig och har laddats in korrekt.")
    return img


def load_and_preprocess_image(file):
    # Öppna bilden med Pillow
    image = Image.open(file.stream)

    # Om bilden har 4 kanaler (RGBA), konvertera den till 3 kanaler (RGB)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
        print("Bilden konverterades från RGBA till RGB.")
    elif image.mode != 'RGB':
        # Om bilden har andra format, konvertera den till RGB
        image = image.convert('RGB')
        print("Bilden konverterades till RGB.")

    # Konvertera till en numpy-array för OpenCV
    img_cv = np.array(image)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)  # Konvertera till OpenCV:s BGR-format

    return img_cv