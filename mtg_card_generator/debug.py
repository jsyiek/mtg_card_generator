import os
import pickle

import mtg_card_generator.data_processing.card_data_aggregator.api_fetch as api_fetch
import mtg_card_generator.generator.generate_card as generate_text
import mtg_card_generator.data_processing.card_data_aggregator.aggregator as aggregator
import mtg_card_generator.generator.render_text as render_text

if __name__ == "__main__":

    chunk_length = 3
    reset = True
    reset_json = False

    if os.path.exists("test_data.dat") and not reset:
        with open("test_data.dat", "rb") as F:
            opening_text, lines_in_text = pickle.load(F)
    else:
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

        tcd, opening_text, lines_in_text = aggregator.gather_data(cards, chunk_length)
        try:
            with open("text_data.dat", "wb+") as F:
                pickle.dump((opening_text, lines_in_text), F)
        except RecursionError:
            pass

    for x in range(50):
        generated_lines = generate_text.generate_text_chunk_list(opening_text, lines_in_text, card_type="Creature")
        cmc = generate_text.determine_cmc(generated_lines)
        colors = generate_text.determine_color(generated_lines)
        power_toughness = generate_text.determine_power_toughness(cmc, generated_lines)
        rarity = generate_text.determine_rarity(generated_lines)
        subtypes = generate_text.determine_subtype(generated_lines)
        rendered_lines = render_text.render_text(generated_lines)
        print(cmc)
        print(colors)
        print("Creature")
        print(subtypes)
        print(power_toughness)
        print(rarity)
        print(rendered_lines, end="\n----------------------------------------------------\n")

    for card_type in ["Instant", "Sorcery", "Enchantment"]:
        for x in range(50):
            generated_lines = generate_text.generate_text_chunk_list(opening_text, lines_in_text, card_type=card_type)
            cmc = generate_text.determine_cmc(generated_lines)
            colors = generate_text.determine_color(generated_lines)
            rarity = generate_text.determine_rarity(generated_lines)
            rendered_lines = render_text.render_text(generated_lines)
            print(cmc)
            print(colors)
            print(card_type)
            print(rarity)
            print(rendered_lines, end="\n----------------------------------------------------\n")

    for x in range(50):
        generated_lines = generate_text.generate_text_chunk_list(opening_text, lines_in_text, card_type="Planeswalker")
        cmc = generate_text.determine_cmc(generated_lines)
        colors = generate_text.determine_color(generated_lines)
        loyalty = generate_text.determine_loyalty(generated_lines)
        rarity = generate_text.determine_rarity(generated_lines)
        rendered_lines = render_text.render_text(generated_lines)
        print(cmc)
        print(colors)
        print("Planeswalker")
        print(loyalty)
        print(rarity)
        print(rendered_lines, end="\n----------------------------------------------------\n")



