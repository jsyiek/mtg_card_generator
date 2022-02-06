from typing import List

import mtg_card_generator.data_processing.template_classes.mtg_text_classes as mtg_text_classes

PUNCTUATION = list(".,?!;:}{'`\"") + ["n't", "'s"]


def render_line(chunk_list: List[mtg_text_classes.TextChunk]):
    rendered_line = ""
    for chunk in chunk_list:
        for word in chunk.text_chunk:
            if word in PUNCTUATION:
                rendered_line += word
            elif word == "~" and rendered_line[-2:] == "~ ":
                pass
            else:
                rendered_line += " " + word

    return rendered_line


def render_text(chunk_list_list: List[List[mtg_text_classes.TextChunk]]):
    return "\n".join(render_line(chunk_list) for chunk_list in chunk_list_list)
