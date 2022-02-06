import nltk


def read_tokens(text):
    words = nltk.tokenize.word_tokenize(text.strip())

    return [w.lower() for w in words]
