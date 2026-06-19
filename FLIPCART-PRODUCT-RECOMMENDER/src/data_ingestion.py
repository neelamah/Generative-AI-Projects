 # initilise verctorstore and add document in vector store.
 
from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from src.data_converter import DataConverter
from src.config import Config


class DataIngestor:
    def __init__(self):
        # created embading HuggingFaceEmbeddings
        self.embedding = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
        
        # initilise astradb database
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipcart_database",  # space name giving while create data base
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE
        )
        
    # inject data with database
    # load_existing=True reuse if it is exist.
    # to create new vector store we need to change load_existing=galse
    def ingest(self,load_existing=True):
        if load_existing == True:
            self.vstore
        
        # calling class DataConverter and iits method
        docs = DataConverter("data/flipkart_product_review.csv").convert()
        
        self.vstore.add_documents(docs)
        
        return self.vstore
        

# we want to run this file directly, not as liberary
# if __name__ == "__main__":
#     ingester = DataIngestor()
#     ingester.ingest(load_existing=False) # we passed false because if not exist , it will create.