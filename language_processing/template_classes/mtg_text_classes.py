from typing import Dict, List, Tuple, Union

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
"""

class TextChunk:
    """
    Stores information about a text chunk from an MTG card.
    Also holds satellite information about cards that have this chunk.
    """
    def __init__(self, text_chunk: str):
        self.text_chunk = text_chunk

        # Other satellite data used for card generation
        self.cmcs: Dict[int, int] = {}
        self.colors: Dict[str, int] = {}
        self.pip_intensity: Dict[int, Dict[int, int]] = {}

        # Information about text that may succeed this
        self.successors: Dict[TextChunk, int] = {}

    def __str__(self):
        return self.text_chunk

    def __hash__(self):
        return hash(self.__str__())

    def register_card(self, card: MTGCard):
        self.cmcs[card["cmc"]] = self.cmcs.setdefault(card["cmc"], 0) + 1

        colors_key = " ".join(card["colors"])
        self.colors[colors_key] = self.colors.setdefault(colors_key, 0) + 1

        pip_intensity_key = sum(1 if c in "WUBRGC" else 0 for c in card["manaCost"])
        self.pip_intensity[card["cmc"]][pip_intensity_key] = self.pip_intensity.setdefault(card["cmc"], {})\
                                                                 .setdefault(pip_intensity_key, 0) + 1

    def register_successor(self, chunk: 'TextChunk'):
        self.successors[chunk] = self.successors.setdefault(chunk, 0) + 1


class CreatureTextChunk:
    """
    Stores some specific information relevant to creatures
    """
    def __init__(self, text_chunk: str):
        super().__init__(text_chunk)

        self.subtypes: Dict[str, int] = {}
        self.num_subtypes: Dict[int, int] = {}
        self.power_toughness: Dict[Tuple[str, str], int] = {}

    def register_card(self, card: MTGCard):
        super().__init__(card)

        for st in card["subtypes"]:
            self.subtypes[st] = self.subtypes.setdefault(st, 0) + 1

        self.num_subtypes[len(card["subtypes"])] = self.num_subtypes.setdefault(len(card["subtypes"]), 0) + 1
        self.power_toughness[(card["power"], card["toughness"])] = self.power_toughness.setdefault((card["power"], card["toughness"]), 0) + 1
