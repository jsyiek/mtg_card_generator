from collections import OrderedDict
from typing import Dict

import mtg_card_generator.data_processing.template_classes.mtg_text_classes as mtg_text_classes
import mtg_card_generator.data_processing.word_processing.tokenizer as tokenizer

CARD_TYPE_TO_CLASS = {
    "Creature": mtg_text_classes.CreatureTextChunk
}


def gather_data(cards: dict, chunk_length: int = 3):
    text_chunk_dictionary: Dict[mtg_text_classes.TextChunk] = {
        "Creature": OrderedDict()
    }

    opening_text = {
        "Creature": OrderedDict()
    }

    lines_in_text = {
        "Creature": OrderedDict()
    }

    for c in cards:
        card_type = c["types"][0]
        if card_type not in CARD_TYPE_TO_CLASS:
            # Not implemented for it so we skip that type
            continue

        lines = c.get("text", "").replace(c["name"], "~").split("\n")

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
                    chunk_object.register_card(c)

                if not is_start:
                    previous_chunk.register_successor(chunk_object)
                else:
                    opening_text[card_type][chunk_object] = opening_text[card_type].setdefault(chunk_object, 0) + 1

                previous_chunk = chunk_object

    return text_chunk_dictionary, opening_text, lines_in_text
