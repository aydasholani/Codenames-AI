import random

def create_words_with_colors(words):
    # Specifiera maxantal för varje färg
    max_counts = {"black": 1, "beige": 7, "blue": 8, "red": 8}
    
    # Välj ett lag (blå eller röd) som får ett extra kort
    extra_color = random.choice(["blue", "red"])
    max_counts[extra_color] += 1

    # Skapa en lista som innehåller rätt antal kort för varje färg
    colors = []
    for color, count in max_counts.items():
        colors.extend([color] * count)

    # Slumpa färgernas ordning
    random.shuffle(colors)
    # Konvertera till en 5x5 matris
    board = [{words[i] : colors[i]} for i in range(0, 25)]
    return board
