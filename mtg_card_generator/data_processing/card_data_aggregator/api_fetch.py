import requests

WEBSITE_URL = "https://api.magicthegathering.io/v1/cards"


def get_cards(**get_arguments) -> dict:
    return requests.get(WEBSITE_URL, get_arguments).json()["cards"]
