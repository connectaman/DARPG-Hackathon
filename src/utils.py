import tiktoken
import re

encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(encoding.encode(text))