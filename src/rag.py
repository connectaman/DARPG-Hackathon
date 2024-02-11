from src.schemas import Document
from src.utils import count_tokens
from typing import List, Union, Optional, Literal
import re

class ChatBot:
    def __init__(self,extractor,chunker,embedder,retriever,llm) -> None:
        self.extractor = extractor
        self.chunker = chunker
        self.embedder = embedder
        self.retriever = retriever
        self.llm = llm
        self.messages = []
        self.setup()

    def setup(self):
        docs = self.extractor.extract()
        docs = self.chunker.chunk_document(docs)
        embed_chunks = []
        for d in docs:
            embed_chunks.append(Document(page_content=d.page_content,embeddings=self.embedder.embed(d)))
        self.docs = embed_chunks

    def run(self,query : str):
        relevant_docs = self.retriever.retrieve(query,documents=self.docs)
        sources = ""
        contact = """
                DEPARTMENT OF ADMINISTRATIVE REFORMS & PUBLIC GRIEVANCES

                5th Floor Sardar Patel Bhawan Sansad Marg New Delhi-110001

                AND

                4th & 6th Floor Jawahar Vyapar Bhawan, HC Mathur Lane, New Delhi, Delhi 110001

                Your valuable suggestions are welcome. Please email to :
                Ms. Jaya Dubey,
                Joint Secretary
                Department of AR & PG,
                Sardar Patel Bhawan
                Parliament Street, New Delhi - 110 001
                Phone: (011) 23360208
                Fax: 011-23360352
                Email: jaya.dubey@nic.in

                Any Grievance sent by email will not be attended to / entertained. Please lodge your grievance at http://pgportal.gov.in

                Help Desk
                For reporting/support on technical issues send email at : cpgrams-darpg@nic.in
         """
        for source_number,source in enumerate(relevant_docs):
            if count_tokens(sources) <= 16000:
                sources += f"<SOURCE> [{source_number+1}] {source.page_content} </SOURCE>"


        template = f"""
        You will be provided sources in <SOURCE> tag, you have to answer the user query using the information provided in the source tag. 
        If no relavent source tag is available then simply reply and pass the email and phone details from <CONTACT> tag so that the user can connect with the team
        to resolve their query.

        SOURCES:
        {sources}

        CONTACT:
        {contact}

        Question or Query : {query}
        """
        self.messages = [{"role": "user", "content": template}]
        stream = self.llm.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=self.messages,
            temperature=0,
            # stream=True,
        )
        response = stream.choices[0].message.content
        response = response.replace("\n","<br>")
        response = response.replace("\\n","<br>")
        return response
 