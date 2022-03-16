from collections import OrderedDict
from typing import Dict, List, Tuple

import mtg_card_generator.probability_calculation as probability_calculation
import mtg_card_generator.data_processing.template_classes.mtg_text_classes as mtg_text_classes
import mtg_card_generator.data_processing.word_processing.tokenizer as tokenizer

CARD_TYPE_TO_CLASS = {
    "Creature": mtg_text_classes.CreatureTextChunk,
    "Instant": mtg_text_classes.TextChunk,
    "Sorcery": mtg_text_classes.TextChunk,
    "Enchantment": mtg_text_classes.TextChunk,
    "Planeswalker": mtg_text_classes.PlaneswalkerTextChunk
}


def gather_data(cards: List[Dict], chunk_length: int = 3) -> Tuple[Dict, Dict, Dict]:
    """
    Scrapes all data from an input list of cards into three dictionaries that
    can be used to generate Magic: The Gathering cards.

    Parameters:
        cards (List[dict]): List of Magic: the Gathering cards from the API
        chunk_length (int): Number of chunks to break the text into (see data_processing.word_processing.tokenizer)
                            In general, larger chunks will lead to more coherent but less original cards.

    Returns:
        Tuple[Dict, Dict, Dict]: Three dictionaries in order; the text chunk dictionary (containing all known text
                                 chunks), a dictionary containing all text chunks that have begun a line, and a
                                 dictionary containing the number of lines in a card.
                                 In each case, the dictionary maps the key to the proportion of times that key has been
                                 observed on cards (i.e. number of lines -> num times that num lines has been seen)
    """
    text_chunk_dictionary = {
        "Creature": OrderedDict(),
        "Instant": OrderedDict(),
        "Sorcery": OrderedDict(),
        "Enchantment": OrderedDict(),
        "Planeswalker": OrderedDict()
    }

    opening_text = {
        "Creature": OrderedDict(),
        "Instant": OrderedDict(),
        "Sorcery": OrderedDict(),
        "Enchantment": OrderedDict(),
        "Planeswalker": OrderedDict()
    }

    lines_in_text = {
        "Creature": OrderedDict(),
        "Instant": OrderedDict(),
        "Sorcery": OrderedDict(),
        "Enchantment": OrderedDict(),
        "Planeswalker": OrderedDict()
    }

    for c in cards:
        card_type = c["types"][0]
        if card_type not in CARD_TYPE_TO_CLASS:
            # Not implemented for it so we skip that type
            continue

        lines = c.get("text", "").replace(c["name"], "~").split("\n")
        i = 1
        while i < len(lines):
            if any(lines[i].startswith(k) for k in [" •", "—"]):
                lines[i] += lines[i+1]
                del lines[i+1]
            else:
                i += 1

        lines_in_text[card_type][len(lines)] = lines_in_text[card_type].setdefault(len(lines), 0) + 1

        tokenized_lines = tokenizer.read_tokens(lines)
        chunkified_lines = [tokenizer.chunkify(t, chunk_length) for t in tokenized_lines]

        for chunkified in chunkified_lines:
            previous_chunk: mtg_text_classes.TextChunk = None
            for i, t in enumerate(chunkified):

                is_start = i == 0
                is_full_stop = i == len(chunkified) - 1
                chunk_hash = mtg_text_classes.text_chunk_hash(t, is_full_stop)

                if chunk_hash not in text_chunk_dictionary[card_type]:
                    chunk_object = CARD_TYPE_TO_CLASS[card_type](t, is_full_stop)
                    chunk_object.register_card(c)
                    text_chunk_dictionary[card_type][chunk_hash] = chunk_object

                else:
                    chunk_object = text_chunk_dictionary[card_type][chunk_hash]
                    try:
                        chunk_object.register_card(c)
                    except Exception as e:
                        print(c)
                        raise e

                if not is_start:
                    previous_chunk.register_successor(chunk_object)
                else:
                    opening_text[card_type][chunk_object] = opening_text[card_type].setdefault(chunk_object, 0) + 1

                previous_chunk = chunk_object

    for card_type in CARD_TYPE_TO_CLASS:
        for text_chunk in text_chunk_dictionary[card_type].values():
            text_chunk.format_probabilities()
        probability_calculation.format_dictionary(opening_text[card_type])
        probability_calculation.format_dictionary(lines_in_text[card_type])

    return text_chunk_dictionary, opening_text, lines_in_text
