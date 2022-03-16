from typing import Dict, List

import requests

WEBSITE_URL = "https://api.magicthegathering.io/v1/cards"


def get_cards(**get_arguments) -> List[Dict]:
    """
    Makes a GET request to the Magic: the Gathering cards API. Returns a list of dictionary of cards.
    See the API website for information on the return format.

    Parameters:
        **get_arguments (Any): Any get arguments you want to pass.

    Returns:
        List[Dict]: List of dictionaries (which represent individual cards). This will be a maximum of 100 cards
                    due to API limitations.
    """
    return requests.get(WEBSITE_URL, get_arguments).json()["cards"]
