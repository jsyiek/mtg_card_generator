from collections import OrderedDict
from typing import Dict, List, Tuple, Union

from mtg_card_generator.probability_calculation import format_dictionary

MTGCard = Dict[str, Union[float, str]]
"""
    Holds data for an MTG card taken from the online API
    {
        "name":"Adamant Will",
        "manaCost":"{1}{W}",
        "cmc":2.0,
        "colors":["White"],
        "colorIdentity":["W"],
        "type":"Instant",
        "types":["Instant"],
        "rarity":"Common",
        "set":"DOM",
        "setName":"Dominaria",
        "text":"Target creature gets +2/+2 and gains indestructible until end of turn. (Damage and effects that say \"destroy\" don't destroy it.)",
        "flavor":"The shield took a year to craft, a month to enchant, and a decade to master—all for one glorious moment.",
        "artist":"Alex Konstad","number":"2","layout":"normal","multiverseid":"442890",
    }
    
    ,{
        "name":"Aven Sentry",
        "manaCost":"{3}{W}",
        "cmc":4.0,"colors":["White"],
        "colorIdentity":["W"],
        "type":"Creature — Bird Soldier",
        "types":["Creature"],
        "subtypes":["Bird","Soldier"],
        "rarity":"Common",
        "set":"DOM",
        "setName":"Dominaria",
        "text":"Flying",
        "flavor":"\"My flock flew from a distant continent ruined by cataclysm and war. Benalia gave us shelter to end our exodus.",
        "artist":"Dan Scott",
        "number":"3",
        "power":"3",
        "toughness":"2",
        "layout":"normal",
        "multiverseid":"442891"
    }
"""


class TextChunk:
    """
    Stores information about a text chunk from an MTG card.
    Also holds satellite information about cards that have this chunk.
    """
    def __init__(self, text_chunk: List[str], is_full_stop: int = 0):
        self.text_chunk = text_chunk
        self.is_full_stop = is_full_stop

        # Other satellite data used for card generation
        self.cmcs: Dict[int, int] = OrderedDict()
        self.colors: Dict[str, int] = OrderedDict()
        self.pip_intensity: Dict[int, Dict[int, int]] = {}
        self.rarities: Dict[str, int] = {}

        # Need to count total number seen
        self.total_cards_registered = 0

        # Information about text that may succeed this
        self.successors: Dict[TextChunk, int] = OrderedDict()

        # To check whether or not the numbers have been formatted.
        self.formatted = False

    def __str__(self):
        return str(self.text_chunk)

    def __hash__(self):
        return text_chunk_hash([self.__str__()], self.is_full_stop)

    def __repr__(self):
        return self.__str__()

    def _lock_if_formatted(func, _=""):
        def inner(self, *args, **kwargs):
            if self.formatted:
                raise ValueError("This text chunk is locked! You cannot modify it.")
            func(self, *args, **kwargs)
        return inner

    @_lock_if_formatted
    def register_card(self, card: MTGCard):
        self.total_cards_registered += 1

        self.cmcs[card["cmc"]] = self.cmcs.setdefault(card["cmc"], 0) + 1

        if "colors" in card:
            colors_key = " ".join(card["colors"])
        else:
            colors_key = "Colorless"
        self.colors[colors_key] = self.colors.setdefault(colors_key, 0) + 1

        if "manaCost" in card:
            pip_intensity_key = sum(1 if c in "WUBRGC" else 0 for c in card["manaCost"])
            self.pip_intensity[card["cmc"]][pip_intensity_key] = self.pip_intensity.setdefault(card["cmc"], OrderedDict())\
                                                                 .setdefault(pip_intensity_key, 0) + 1

        if "rarity" in card:
            self.rarities[card["rarity"]] = self.rarities.get(card["rarity"], 0) + 1

    @_lock_if_formatted
    def register_successor(self, chunk: 'TextChunk'):
        self.successors[chunk] = self.successors.setdefault(chunk, 0) + 1

    @_lock_if_formatted
    def format_probabilities(self):
        format_dictionary(self.cmcs)
        format_dictionary(self.colors)
        for cmc in self.pip_intensity:
            format_dictionary(self.pip_intensity[cmc])
        format_dictionary(self.rarities)
        format_dictionary(self.successors)

        self.formatted = True


class CreatureTextChunk(TextChunk):
    """
    Stores some specific information relevant to creatures
    """
    def __init__(self, text_chunk: List[str], is_full_stop: int = 0):
        super().__init__(text_chunk, is_full_stop)

        self.subtypes: Dict[str, int] = {}
        self.num_subtypes: Dict[int, int] = {}
        self.power_toughness: Dict[int, Dict[Tuple[str, str], int]] = {}

    @TextChunk._lock_if_formatted
    def register_card(self, card: MTGCard):
        super().register_card(card)

        if "subtypes" in card:
            for st in card["subtypes"]:
                self.subtypes[st] = self.subtypes.setdefault(st, 0) + 1

            self.num_subtypes[len(card["subtypes"])] = self.num_subtypes.setdefault(len(card["subtypes"]), 0) + 1

        if "power" in card and "toughness" in card and "cmc" in card:
            self.power_toughness[card["cmc"]][(card["power"], card["toughness"])] = self.power_toughness.setdefault(card["cmc"], {})\
                                                                                       .get((card["power"], card["toughness"]), 0) + 1

    @TextChunk._lock_if_formatted
    def format_probabilities(self):
        format_dictionary(self.subtypes)
        format_dictionary(self.num_subtypes)
        for cmc in self.power_toughness:
            format_dictionary(self.power_toughness[cmc])

        super().format_probabilities()


class PlaneswalkerTextChunk(TextChunk):
    """
    Stores extra Planeswalker-specific information:
        loyalty_counters (Dict[int, int]): Maps number of starting loyalty counters to observed instances
    """

    def __init__(self, text_chunk: List[str], is_full_stop: int = 0):
        super().__init__(text_chunk, is_full_stop)

        self.loyalty_counters: Dict[int, int] = {}

    @TextChunk._lock_if_formatted
    def register_card(self, card: MTGCard):
        super().register_card(card)

        if "loyalty" in card:
            self.loyalty_counters[card["loyalty"]] = self.loyalty_counters.get(card["loyalty"], 0) + 1

    @TextChunk._lock_if_formatted
    def format_probabilities(self):
        format_dictionary(self.loyalty_counters)

        super().format_probabilities()


def text_chunk_hash(chunk: List[str], is_full_stop: bool):
    return hash("".join(chunk)) + is_full_stop
