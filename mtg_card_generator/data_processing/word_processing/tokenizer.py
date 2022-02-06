import nltk

from typing import List


def read_tokens(text: List[str]):
    lines = []
    for line in text:
        lines.append(nltk.tokenize.word_tokenize(line.strip()))

    return [[w.lower() for w in words] for words in lines]


def chunkify(text: List[str], n: int):
    return [text[i:i+n] for i in range(0, len(text), n)]
