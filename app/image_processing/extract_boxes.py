def extract_boxes(results, card_class=0, textbox_class=1):
    """Extracts bounding boxes for cards and textboxes from YOLO model results."""
    card_boxes = []
    textbox_boxes = []
    for result in results:
        for box in result.boxes:
            cls = int(box.cls.item())
            x1, y1, x2, y2 = [int(coord.item()) for coord in box.xyxy[0]]
            if cls == card_class:
                card_boxes.append((x1, y1, x2, y2))
            elif cls == textbox_class:
                textbox_boxes.append((x1, y1, x2, y2))
    return card_boxes, textbox_boxes