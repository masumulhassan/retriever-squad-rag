import os
from dotenv import load_dotenv

load_dotenv()

model_configs = {
    'LLM_URI': os.getenv("LLM_URI", "http://localhost:11434"),
    'EMBEDDING_MODEL': os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
    'GENERATIVE_MODEL': os.getenv("GENERATIVE_MODEL", "llama3.2:1b"),
}

document_store_configs = {
    'MILVUS_URI': os.getenv("MILVUS_URI", "http://localhost:19530"),
}

dataset_configs = {
    'DATA_PATH': os.getenv("DATA_PATH", "/Users/masumulhassan/PycharmProjects/haystack-with-streamlit/dataset")
}
