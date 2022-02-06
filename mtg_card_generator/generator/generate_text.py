import random


def select_random(dictionary):
    return random.choices(list(dictionary.keys()), weights=list(dictionary.values()))[0]


def generate_text(opening_text, lines_in_text, card_type: str = "Creature"):
    num_lines = select_random(lines_in_text[card_type])
    lines = []
    for i in range(num_lines):
        current_chunk = select_random(opening_text[card_type])
        current_line = [current_chunk]

        # Every card will eventually lead to a full stop
        while not current_chunk.is_full_stop:
            current_chunk = select_random(current_chunk.successors)
            current_line.append(current_chunk)


        lines.append(current_line)

    return lines
