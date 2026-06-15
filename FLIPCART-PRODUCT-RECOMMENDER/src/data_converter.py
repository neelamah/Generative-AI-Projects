import pandas as pd
from langchain_core.documents import Document
from langchain_community.document_loaders import CSVLoader

#Document  ->  before creating chunks , we need to convert in document LangChain’s whole pipeline (chunking → embeddings → vector DB → retrieval) is designed to work with Document objects.
#itcan be done manually or used built in loaders (CSVLoader, Textloader,  PypdfLoader,WebbaseLoader, WikipediaLoader)

class DataConverter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def convert(self):
        #CSVLoader -> automatically convert in document when it load. we can't select perticular column on which we want to aplly.
        #pd.read_csv -> if we use this we need to convert manuaaly in document. and also can select column ehich we want.
        loader = CSVLoader(file_path=self.file_path)
        documents = loader.load()
      
        # for each row  it will create as seprate document
        # df= pd.read_csv(self.file_path)[["product_title", "review"]]
        # documents = [
        #     Document(page_content=row['review'] , metadata = {"product_name" : row["product_title"]})
        #     for _, row in df.iterrows()
        # ]
      
        print(documents)
        return documents
    
# we want to run this file directly, not as liberary
# if __name__ == "__main__":
#     file_path = "data/flipkart_product_review.csv"
#     data_converter = DataConverter(file_path)
#     data_converter.convert()