from typing import List

import mtg_card_generator.data_processing.template_classes.mtg_text_classes as mtg_text_classes

PUNCTUATION = list(".,?!;:'`\"") + ["n't", "'s"]


def render_line(chunk_list: List[mtg_text_classes.TextChunk]) -> str:
    """
    Takes in a list of text chunks and returns a string representing the text chunks joined together.

    Parameters:
        chunk_list (List[mtg_text_classes.TextChunk]): A list of text chunks to be turned into a rendered line.

    Returns:
        str: The line rendered as a string
    """
    rendered_line = ""
    for chunk in chunk_list:
        for word in chunk.text_chunk:
            # No need to put a space before punctuation.
            if word in PUNCTUATION:
                rendered_line += word
            elif word == "~" and rendered_line[-2:] == "~ ":
                pass
            else:
                rendered_line += " " + word

    return rendered_line


def render_text(chunk_list_list: List[List[mtg_text_classes.TextChunk]]):
    """
    Renders a list of lines using render_line

    Parameters:
        chunk_list_list (List[List[mtg_text_classes.TextChunk]]): A list of lines on to render, where each line is
                                                                  represented by a list of chunks.
    """
    return "\n".join(render_line(chunk_list) for chunk_list in chunk_list_list)
