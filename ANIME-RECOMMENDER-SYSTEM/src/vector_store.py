#creating db

# function create vector store if not exisits
#function to load vectoe store if it exists and return the Chroma object

from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv()

#CharacterTextSplitter -> splity documents into smaller chunks, 
# which is important for better performance when creating embeddings and querying the vector store.

#It does 3 things automatically:

#Takes your documents
#HuggingFaceEmbeddings -> Converts them into embeddings
#persist_directory = it will create a directory called chroma_db and store the vector store there. You can change this to any directory you want.

# creatte vector store builder class
#persist_directory: str="chroma_db"
class VectorStoreBuilder:
    def __init__(self, csv_path: str, persist_dir: str="chroma_db"):
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        

    def build_and_save_vectorstore(self):
        # Load the processed CSV file using CSVLoader
        loader = CSVLoader(
            file_path= self.csv_path, 
            encoding='utf-8'
            )
        
        documents = loader.load()

        # Split the documents into smaller chunks using CharacterTextSplitter
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_documents = text_splitter.split_documents(documents)
        
        
    

        #Create vector DB using Chroma and persist it to disk 
        db = Chroma.from_documents(
             split_documents, #it will take split documents as input
             embedding=self.embeddings_model, #it will use the HuggingFaceEmbeddings model to convert the documents into embeddings
             persist_directory=self.persist_dir #it will create a directory called chroma_db and store the vector store there. You can change this to any directory you want.
            )
        
        db.persist()
        
    #function to load the vector store from disk, if it is exists, and return the Chroma object. 
    # This will allow you to query the vector store later on.
    def load_vector_store(self):
        db = Chroma(
            embedding_function=self.embeddings_model, #it will use the HuggingFaceEmbeddings model to convert the documents into embeddings
            persist_directory=self.persist_dir #it will load the vector store from the directory where it was saved
        )
        return db
   