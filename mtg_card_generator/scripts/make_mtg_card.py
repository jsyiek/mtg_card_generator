"""
Command-line script to generate an MTG card
"""

import argparse

from typing import List

import mtg_card_generator.generator.generate_card as generate_card
import mtg_card_generator.data_processing.card_data_aggregator.initialize_aggregated_data as initialize


def parse_args():
    parser = argparse.ArgumentParser("Generate MTG cards on the command line!")

    parser.add_argument("-c", "--card-type", help="Card type to generate. You can enter multiple and it will "
                                                  "generate `n` for each instance entered. Defaults to creature.",
                        nargs="+", choices=["Creature", "Enchantment", "Instant", "Sorcery", "Planeswalker"],
                        default=["Creature"])
    parser.add_argument("-n", "--number", help="Number of cards to generate. For each card type inputted, "
                                               "this generates `n` cards of that type.",
                        type=int, default=1)
    parser.add_argument("-mo", "--markov-order", help="Order of Markov Model to use. Higher orders increase how much "
                                                      "grammatical sense the cards make while reducing creativity."
                                                      "Defaults to third order, which I find tends to perform the "
                                                      "best.",
                        default=3, type=int)
    parser.add_argument("--reset-json", help="Forces the program to completely reload its data. This will update it "
                                             "to include the most recent cards, but this will take a significant "
                                             "amount of time.",
                        action="store_true")

    return parser.parse_args()


def main():
    args = parse_args()

    text_chunk_dictionary, opening_text, lines_in_text = initialize.initialize_aggregated_data(args.markov_order,
                                                                                               args.reset_json)

    for card_type in args.card_type:
        for i in range(args.number):
            card = generate_card.generate_card(opening_text, lines_in_text, card_type)
            print(card)


if __name__ == "__main__":
    main()
