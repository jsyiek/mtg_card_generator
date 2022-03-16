import logging
import os
import pickle

from typing import Tuple

from mtg_card_generator import REPOSITORY_PATH
import mtg_card_generator.data_processing.card_data_aggregator.api_fetch as api_fetch
import mtg_card_generator.data_processing.card_data_aggregator.aggregator as aggregator


__CARDS_CACHE_PATH = os.path.join(REPOSITORY_PATH, "mtg_card_generator", "data", "cards_json.dat")

this_logger = logging.getLogger()

def initialize_aggregated_data(chunk_length=3, reset_json=False) -> Tuple[dict, dict, dict]:
    """
    Loads the parameters for the Markov Model. Can also be used to reload the card data json.

    Parameters:
        chunk_length (int): Order of Markov Model to use, i.e. number of words in a row to consider a node
        reset_json (bool): Whether to reload the card data or not.

    Returns:
        Tuple[dict, dict, dict]: See aggregator.gather_data
    """

    if reset_json or not os.path.exists(__CARDS_CACHE_PATH):
        this_logger.warning("Either JSON reset has been requested or the cache file could not be found. "
                            "A new cache file will be generated. This may take some time.")
        cards = []
        next_cards = api_fetch.get_cards(page = 0)
        cards.extend(next_cards)
        i = 1
        while len(next_cards) == 100:
            this_logger.info(f"Calling API, page: {i}")
            next_cards = api_fetch.get_cards(page=i)
            cards.extend(next_cards)
            i += 1

        this_logger.info("API calls complete. Caching...")

        with open(__CARDS_CACHE_PATH, "wb+") as F:
            pickle.dump(cards, F)

        this_logger.info("Caching succeeded.")

    else:
        this_logger.info("Loading cached files...")
        with open(__CARDS_CACHE_PATH, "rb") as F:
            cards = pickle.load(F)

    this_logger.info("Training model...")
    return aggregator.gather_data(cards, chunk_length)
