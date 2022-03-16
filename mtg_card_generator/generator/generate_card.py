import random

from collections import OrderedDict
from fractions import Fraction
from typing import Any, Dict, List, Union

import mtg_card_generator.generator.probability_calculation as probability_calculation
import mtg_card_generator.data_processing.template_classes.mtg_text_classes as mtg_text_classes
import mtg_card_generator.generator.render_text as render_text


COLORS_TO_PIP = {
    'Black': 'B',
    'Blue': 'U',
    'Colorless': 'C',
    'Green': 'G',
    'Red': 'R',
    'White': 'W'
}


def select_random(dictionary: OrderedDict) -> Any:
    """
    Selects a random key from the dictionary. The random choice is weighted by the integer
    values that the key corresponds to

    Parameters:
        dictionary (OrderedDict[Any, int]): Dictionary mapping item to its weighting

    Returns:
        Any: Random key from the dictionary weighted by the integer they correspond to
    """
    return random.choices(list(dictionary.keys()), weights=list(dictionary.values()))[0]


def generate_card(opening_text: Dict[mtg_text_classes.TextChunk, int],
                  lines_in_text: Dict[int, int],
                  card_type: str = "Creature") -> mtg_text_classes.MTGCard:
    """
    Generates a random Magic: the Gathering card
    Parameters:
        opening_text (Dict[mtg_text_classes.TextChunk]): Mapping a text chunk that has been observed
                                                      to begin a line to the number of times it has lead that line
                                                      (or some other equivalent weighting)
        lines_in_text (Dict[int, int]): Mapping the number of lines in an observed card to the number of times
                                     we've seen cards with that number of lines.
        card_type (str): Card type to generate

    Returns:
        MTGCard: A dictionary with a set of fields for the card
    """
    generated_lines = generate_text_chunk_list(opening_text, lines_in_text, card_type=card_type)

    cmc = determine_cmc(generated_lines)
    colors = determine_color(generated_lines)
    pip_intensity = determine_pip_intensity(cmc, generated_lines)
    rendered_lines = render_text.render_text(generated_lines)
    contains_x = ' x ' in rendered_lines

    generated_card = {
        'cmc': cmc,
        'colors': colors,
        'manacost': determine_mana_cost(pip_intensity, cmc, colors, contains_x),
        'type': card_type,
        'rendered_lines': rendered_lines,
        'rarity': determine_rarity(generated_lines),
    }

    if card_type == "Creature":
        generate_creature_parameters(generated_lines, card_generated_so_far=generated_card)

    return generated_card


def generate_creature_parameters(generated_lines: List[List[mtg_text_classes.TextChunk]],
                                 card_generated_so_far: mtg_text_classes.MTGCard):
    """
    Helper function to generate extra parameters that are required for creature cards
    """
    generate_card = {
        'power_toughness': determine_power_toughness(card_generated_so_far['cmc'], generated_lines),
        'subtypes': determine_subtype(generated_lines)
    }
    card_generated_so_far.update(generate_card)


def generate_text_chunk_list(opening_text: Dict[mtg_text_classes.TextChunk, int],
                             lines_in_text: Dict[int, int],
                             card_type: str = "Creature") -> List[List[mtg_text_classes.TextChunk]]:
    """
    Takes in a set of generated parameters and, for a given card type, generates
    a random list of lists of text chunks representing a card of that type.
    Each list within the list of lists corresponds to line on that card.

    Parameters:
         opening_text (Dict[mtg_text_classes.TextChunk]): Mapping a text chunk that has been observed
                                                          to begin a line to the number of times it has lead that line
                                                          (or some other equivalent weighting)
         lines_in_text (Dict[int, int]): Mapping the number of lines in an observed card to the number of times
                                         we've seen cards with that number of lines.
         card_type (str): Card type to generate

    Returns:
        List[List[mtg_text_classes.TextChunk]]: List of lines, each represented as a list of TextChunks
    """
    num_lines = select_random(lines_in_text[card_type])
    lines = []
    for i in range(num_lines):
        current_chunk = select_random(opening_text[card_type])
        current_line = [current_chunk]

        # Every card will eventually lead to a full stop
        # This will eventually terminate
        while not current_chunk.is_full_stop:
            current_chunk = select_random(current_chunk.successors)
            current_line.append(current_chunk)

        lines.append(current_line)

    return lines


def determine_random_card_variable(lines: List[List[mtg_text_classes.TextChunk]],
                                   var_names: List[str]) -> Union[int, str]:
    """
    Given a set of lines on a card(i.e. list of lists of text chunks), this function chooses a random variable that is
    to be the attribute of the card. The random selection is weighted according to the number of times we have
    seen these particular attributes appear on cards in the past.

    Assumes that each TextChunk is independent of the others and that the overall probability of a trait being
    associated with the group is all the probabilities multiplied together.

    Parameters:
        lines (List[List[TextChunk]): Generated rules text for the card
        var_names (List[str]): The variables needed to input to the dictionary to get the chances

    Returns:
        Union[int, str]: The trait in question that we want to determine
    """
    probability_dict = {}
    fallback_total = 1
    for l in lines:
        for text_chunk in l:
            dictionary_to_use = vars(text_chunk)[var_names[0]]
            for i in range(1, len(var_names)):
                dictionary_to_use = dictionary_to_use.get(var_names[i], {})

            probability_dict = probability_calculation.multiply_probability(
                probability_dict,
                dictionary_to_use,
                Fraction(1, fallback_total),
                Fraction(1, text_chunk.total_cards_registered)
            )
            fallback_total *= text_chunk.total_cards_registered

    try:
        return select_random(probability_dict)
    except:
        print("t")
        exit()

def determine_cmc(lines: List[List[mtg_text_classes.TextChunk]]):
    return int(determine_random_card_variable(lines, ["cmcs"]))


def determine_color(lines: List[List[mtg_text_classes.TextChunk]]):
    colors = determine_random_card_variable(lines, ["colors"])
    return [COLORS_TO_PIP[c] for c in colors.split()]


def determine_pip_intensity(cmc: int, lines: List[List[mtg_text_classes.TextChunk]]):
    if cmc == 0:
        return 0
    return determine_random_card_variable(lines, ["pip_intensity", cmc])


def determine_power_toughness(cmc: int, lines: List[List[mtg_text_classes.TextChunk]]):
    return determine_random_card_variable(lines, ["power_toughness", cmc])


def determine_rarity(lines: List[List[mtg_text_classes.TextChunk]]):
    return determine_random_card_variable(lines, ["rarities"])


def determine_subtype(lines: List[List[mtg_text_classes.TextChunk]]):
    return determine_random_card_variable(lines, ["subtypes"])


def determine_loyalty(lines: List[List[mtg_text_classes.TextChunk]]):
    return determine_random_card_variable(lines, ["loyalty_counters"])


def determine_mana_cost(pip_intensity: int, cmc: int, colors: List[str], contains_x: bool = False) -> str:
    """
    Determines the mana cost of the card. This can be uniquely determined from its
    pip_intensity (the number of non-generic mana symbols in its cost), its converted
    mana cost, and the variety of different colors in its cost.
    """
    cost = []
    if cmc > pip_intensity:
        cost.append(str(cmc - pip_intensity))
    while pip_intensity >= len(colors):
        cost += colors
        pip_intensity -= len(colors)
    while pip_intensity > 0:
        cost.append(random.choice(colors))
        pip_intensity -= 1
    mana_cost = "".join(cost)
    mana_cost = "".join(sorted(list(mana_cost)))
    if contains_x:
        mana_cost = "X" + mana_cost
    return mana_cost
