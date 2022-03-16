import nltk

from typing import List


def read_tokens(text: List[str]) -> List[List[str]]:
    """
    Tokenizes a list of sentences.

    Parameters:
        text (List[str]): List of lines to tokenize into a list of lists of token.

    Returns:
        tokenized_text (List[List[str]]): List of lists of tokens (each inner list represents a line
    """
    lines = []
    for line in text:
        lines.append(nltk.tokenize.word_tokenize(line.strip()))

    return [[w.lower() for w in words] for words in lines]


def chunkify(text: List[str], n: int) -> List[List[str]]:
    """
    Breaks a list of tokens in each line into a list of lists of tokens, where each inner list has length n

    Parameters:
          text (List[str]): Line to chunkify
          n (int): Number of items in each chunk

    Returns:
          text (List[List[str]]): List of n-lists representing the chunkified data.
    """
    return [text[i:i+n] for i in range(0, len(text), n)]
