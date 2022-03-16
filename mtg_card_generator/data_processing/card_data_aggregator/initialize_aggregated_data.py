import pickle

from typing import Tuple

import mtg_card_generator.data_processing.card_data_aggregator.api_fetch as api_fetch
import mtg_card_generator.data_processing.card_data_aggregator.aggregator as aggregator


def initialize_aggregated_data(chunk_length=3, reset_json=False) -> Tuple[dict, dict, dict]:
    """
    Loads the parameters for the Markov Model. Can also be used to reload the card data json.

    Parameters:
        chunk_length (int): Order of Markov Model to use, i.e. number of words in a row to consider a node
        reset_json (bool): Whether to reload the card data or not.

    Returns:
        Tuple[dict, dict, dict]: See aggregator.gather_data
    """

    if reset_json:
        cards = []
        next_cards = api_fetch.get_cards(page = 0)
        cards.extend(next_cards)
        i = 1
        while len(next_cards) == 100:
            print(i)
            next_cards = api_fetch.get_cards(page=i)
            cards.extend(next_cards)
            i += 1

        with open("text_json.dat", "wb+") as F:
            pickle.dump(cards, F)

    else:
        with open("text_json.dat", "rb") as F:
            cards = pickle.load(F)

    return aggregator.gather_data(cards, chunk_length)
