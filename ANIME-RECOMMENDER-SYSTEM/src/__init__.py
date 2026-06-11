#create db using data
from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting the data loading and vector store building process...")
        
        # Step 1: Load and process the data
        loader = AnimeDataLoader("data/anime_with_synopsis.csv" , "data/anime_updated.csv")
        processed_csv = loader.load_and_process()
 
        logger.info("Data  loaded and processed...")
        
        # Step 2: Build and save the vector store
        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_and_save_vectorstore()
        
        logger.info("Vector store Built sucesfully....")
        logger.info("Pipelien built sucesfuly....")
        
    except Exception as e:
        logger.error(f"Failed to execute pipeline {str(e)}")
        raise CustomException(f"Error in main function: {e}")
    
    if __name__=="__main__":
     main()