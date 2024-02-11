from src.extractor import PDFExtractor
from src.chunker import Chunk
from src.embedder import BGEEmbedder
from src.retriever import DenseRetriever
from src.schemas import Document
from src.rag import ChatBot
from openai import OpenAI
from flask import Flask, render_template, request
import os

import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)

logging.info(" Loading Documents")
extractor = PDFExtractor(pdf_path="/workspaces/DARPG-Hackathon/data/pdf")
chunker = Chunk()
bge = BGEEmbedder()
dense = DenseRetriever(embedder=bge)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY",""))
chat = ChatBot(extractor=extractor,chunker=chunker,embedder=bge,retriever=dense,llm=client)
logging.info(" Object Creation Done")

app = Flask(__name__)

@app.route("/chatbot")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chat.run(userText))
app.run(debug = True)