import cv2
import os
import json

def save_card_images(img, card_boxes, recognized_texts, image_name):
    """Saves each detected card as an image and records data in JSON format."""
    output_dir = os.path.join(os.getcwd(), "modelv12", "results", image_name)
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(os.path.join(output_dir, "board.png"), img)
    json_data = []
    
    for i, (box, text) in enumerate(zip(card_boxes, recognized_texts), start=1):
        x1, y1, x2, y2 = box
        card_img = img[y1:y2, x1:x2]
        
        # Save each image
        output_card_path = os.path.join(output_dir, f"card_{i}.png")
        cv2.imwrite(output_card_path, card_img)
        

        card_info = {
            "word": text,
            "card_position": i,
            "word": text,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        }
        
        json_data.append(card_info)

    

    json_path = os.path.join(output_dir, "card_data.json")
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)
