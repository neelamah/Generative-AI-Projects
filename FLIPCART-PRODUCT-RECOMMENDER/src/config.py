import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    #copying the environment variables from .env file to the Config class
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5" #huggingface embading  model we are not including here  hugging face token beacause it is not required for this model. 
    RAG_MODEL = "llama-3.1-8b-instant"   #groq model