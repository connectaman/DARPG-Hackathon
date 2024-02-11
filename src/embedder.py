from src.schemas import Document
from typing import List, Union
from transformers import AutoTokenizer, AutoModel
import torch


class BGEEmbedder():
    def __init__(
        self,
        model_name='BAAI/bge-large-en-v1.5',
    ) -> None:
        """
        Initialize the API client with the specified API URL, route, payload, headers, and request method.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        

    def embed(self, text: Union[str, Document]) -> Document:
        if isinstance(text,str):
            encoded_input = self.tokenizer([text], padding=True, truncation=True, return_tensors='pt')
        elif isinstance(text,Document):
            encoded_input = self.tokenizer([text.page_content], padding=True, truncation=True, return_tensors='pt')
        else:
            raise Exception("Unable to embed")
        
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            # Perform pooling. In this case, cls pooling.
            sentence_embeddings = model_output[0][:, 0]
        # normalize embeddings
        sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1).tolist()[0]

        return sentence_embeddings
