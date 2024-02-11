from typing import List, Literal, Optional
from pydantic import Field

class Document:
    def __init__(self, page_content: str,tokens : int = 0, embeddings=[], metadata: dict = {}) -> None:
        self.page_content = page_content
        self.tokens = tokens
        self.embeddings = embeddings
        self.metadata = metadata

    def __repr__(self):
        return repr(self.__dict__)
