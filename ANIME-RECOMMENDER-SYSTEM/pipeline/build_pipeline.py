# this pipe line is only to load data, process it and create vector store
from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting to build pipeline...")

        # Load and process data from data_loader file
        loader = AnimeDataLoader("data/anime_with_synopsis.csv" , "data/anime_updated.csv")
        processed_csv = loader.load_and_process()

        logger.info("Data  loaded and processed...")

        # Build vector store from processed data and save it using vector_store file
        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_and_save_vectorstore()

        logger.info("Vector store Built sucesfully....")

        logger.info("Pipelien built sucesfuly....")
    except Exception as e:
            logger.error(f"Failed to execute pipeline {str(e)}")
            raise CustomException("Error during pipeline " , e)
    
if __name__=="__main__":
     main()