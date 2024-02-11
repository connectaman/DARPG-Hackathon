from src.schemas import Document
from typing import List, Union
import numpy as np
import faiss

class DenseRetriever():
    def __init__(self, embedder, **kwargs) -> None:
        """
        Initializes the class with the given chunks and documents.

        Parameters:
            chunks (List[Chunk]): List of Chunk objects.
            documents (List[Document]): List of Document objects.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        documents: List[Document] = None,
        similarity_score: float = 0.6,
        top_k: int = 10,
        **kwargs
    ) -> List[Union[Document]]:
        """
        Retrieves and returns a list of chunks or documents based on the given query and embedding model.

        Args:
            query (str): The query string to retrieve chunks or documents.
            embedder: The embedding model to use for retrieving chunks or documents.
            similarity_score (float): The similarity score threshold. Defaults to 0.6.
            top_k (int): The maximum number of chunks or documents to return. Defaults to 10.
            **kwargs: Additional keyword arguments.

        Returns:
            List[Union[Chunk, Document]]: The list of chunks or documents based on the query and embedding model.
        """
      
        self.documents = documents
        if self.documents is not None:
            self.embeddings_array = np.array(
                [document.embeddings for document in documents], dtype=np.float32
            )
            self.n, self.d = self.embeddings_array.shape
            self.db = faiss.IndexFlatIP(self.d)
            self.db.add(self.embeddings_array)
        else:
            raise ("Not supported format")

        if self.embedder is None:
            raise Exception("Kindly pass Embedding Model")
        embed_query = np.array([self.embedder.embed(text=query)],dtype='float32')
        _, scores, row_ids = self.db.range_search(
            x=embed_query, thresh=similarity_score
        )
        scores = np.array(scores)
        row_ids = np.array(row_ids)
        idx = np.flip(np.argsort(scores))
        scores = np.array(scores)[idx]
        row_ids = np.array(row_ids)[idx]
        if self.documents is not None:
            for i, j in enumerate(row_ids):
                self.documents[i], self.documents[j] = (
                    self.documents[j],
                    self.documents[i],
                )
            return self.documents[: min(top_k, len(self.documents))]
        else:
            raise Exception(
                "format not supported please provide either chunk or documents"
            )
