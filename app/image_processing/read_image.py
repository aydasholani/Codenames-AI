import cv2

def read_image(image_path):
    """Reads an image from the specified path."""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Unable to read the image: {image_path}")
    return img