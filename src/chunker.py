from src.schemas import Document
from src.utils import count_tokens
from typing import Dict, List

class Chunk():
    """
    __init__: Initializes a SlidingWindowChunk object and sets default values for chunk_size and chunk_overlap.
    set_chunk: Sets the chunk text to the given input.
    get_chunk: Returns the chunk text.
    """

    def __init__(
        self,
        chunk_size: int = 450,
        chunk_overlap: int = 50,
        **kwargs
    ):
        """
        Initializes a SlidingWindowChunk object.

        Parameters:
            **kwargs: additional keyword arguments

        Returns:
            None
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunked_documents = []

    def get_chunks(self):
        """
        Return the chunk text.
        """
        return self.chunked_documents

    def chunk_document(self,documents : List[Document]) -> List[Document]:
        """
        Chunk the documents using sliding window.

        Args:
            documents (List[Document]): The list of documents to be chunked.

        Returns:
            List[Document]: The list of chunked documents.
        """
        for document in documents:
            doc_content = document.page_content
            words = doc_content.split()
            start = 0
            end = self.chunk_size

            while start < len(words):
                doc_chunk = ' '.join(words[start:end])
                self.chunked_documents.append(Document(page_content = doc_chunk, tokens = count_tokens(doc_chunk)))
                start += self.chunk_size - self.chunk_overlap
                end += self.chunk_size + self.chunk_overlap

        return self.chunked_documents

    def __repr__(self):
        return repr(self.__dict__)
