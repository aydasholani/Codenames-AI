def sort_boxes(card_boxes, tolerance=50):
    if not card_boxes:
        return []

    # Sortera korten först efter Y-position (rad för rad)
    card_boxes.sort(key=lambda b: (b[1], b[0]))

    # Gruppera korten i rader baserat på Y-positionen
    rows = []
    current_row = [card_boxes[0]]
    
    for box in card_boxes[1:]:
        # Kontrollera om kortet är i samma rad genom att jämföra Y-koordinaterna med tolerans
        if abs(box[1] - current_row[-1][1]) < tolerance:
            current_row.append(box)
        else:
            rows.append(current_row)
            current_row = [box]

    rows.append(current_row)  # Lägg till sista raden

    # Sortera varje rad från vänster till höger baserat på X-position
    sorted_cards = [card for row in rows for card in sorted(row, key=lambda b: b[0])]

    return sorted_cards