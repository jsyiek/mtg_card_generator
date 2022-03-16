from fractions import Fraction
from typing import Any, Dict


def format_dictionary(dictionary: Dict[Any, int]) -> Dict[Any, int]:
    """
    Takes a dictionary representing counts and normalizes it such that each
    variable is between 0 and 1. Analogous to process for normalizing a
    vector.

    Parameters:
        dictionary (Dict[Any, int]): The dictionary to normalize

    Returns:
        Dict[Any, int]: Normalized dictionary
    """
    sum_dict = sum(v for v in dictionary.values())
    for k, v in dictionary.items():
        dictionary[k] = Fraction(v, sum_dict)
    return dictionary


def multiply_probability(d1: Dict[Any, int], d2: Dict[Any, int], fallback_d1=1, fallback_d2=1):
    """
    Multiplies the keys of two dictionaries. If a key isn't present in one of them, the fallback value
    for that dictionary is used.

    Parameters:
        d1 (Dict[Any, int]): First dictionary to combine
        d2 (Dict[Any, int]): Second dictionary to combine
        fallback_d1 (int): First dictionary fallback value (defaults to 1)
        fallback_d2 (int): Second dictionary fallback value (defaults to 1)

    Returns:
        Dict[Any, int]: The combined dictionary
"""
    return_dict = {}
    for k in set(d1.keys()).union(d2.keys()):
        return_dict[k] = d1.get(k, fallback_d1) * d2.get(k, fallback_d2)
    return return_dict
