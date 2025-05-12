import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv, find_dotenv
import chromadb.utils.embedding_functions as emb_functions
from datetime import datetime

from common.my_config import MyConfig

config = MyConfig()

openai_ef = emb_functions.OpenAIEmbeddingFunction(
    api_key=config.embedding_api_key,
    model_name=config.embedding_model_name,
    api_base=config.embedding_api_base
)


class My_Chroma:
    def __init__(self):
        self.db_path = config.vdb_path
        self.client = self.get_client(path=self.db_path)
        self.qa_collection = self.get_collection(config.qa_collection_name)
        self.doc_collection = self.get_collection(config.doc_collection_name)

    def get_client(self, path):
        client = chromadb.PersistentClient(path=path)
        return client

    def get_collection(self, collection_name):
        return self.client.get_or_create_collection(name=collection_name, embedding_function=openai_ef,

                                                    metadata={"create_time": str(datetime.now())})

    def delete_collection(self, collection_name):
        self.client.delete_collection(name=collection_name)
