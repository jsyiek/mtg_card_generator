import os
import pickle

import mtg_card_generator.data_processing.card_data_aggregator.api_fetch as api_fetch
import mtg_card_generator.generator.generate_text as generate_text
import mtg_card_generator.data_processing.card_data_aggregator.aggregator as aggregator
import mtg_card_generator.generator.render_text as render_text

if __name__ == "__main__":
    chunk_length = 2
    get_args = {}
    reset = False

    if os.path.exists("test_data.dat") and not reset:
       with open("test_data.dat", "rb") as F:
            opening_text, lines_in_text = pickle.load(F)
    else:
        cards = api_fetch.get_cards(**get_args)
        tcd, opening_text, lines_in_text = aggregator.gather_data(cards, chunk_length)
        with open("text_data.dat", "wb+") as F:
            pickle.dump((opening_text, lines_in_text), F)

    for x in range(50):
        generated_lines = generate_text.generate_text(opening_text, lines_in_text)
        rendered_lines = render_text.render_text(generated_lines)
        print(rendered_lines, end="\n----------------------------------------------------\n")
