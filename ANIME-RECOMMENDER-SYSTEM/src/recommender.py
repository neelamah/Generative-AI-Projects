# creating query chain to query from vector store using llm , prompt and retriever and run to get output

#create recommender class that will use the vector store and the prompt template to generate recommendations based on user query.
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from src.prompt_template import get_anime_prompt

class AnimeRecommender:
    def __init__(self,retriever,api_key:str,model_name:str):
        self.retriever = retriever
        self.api_key = api_key
        self.model_name = model_name
        self.prompt = get_anime_prompt()
        self.llm = ChatGroq(api_key=self.api_key, model=self.model_name)
        
    def generate_recommendations(self, query: str):
        # Create a RetrievalQA chain using the retriever and the prompt template
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
        
        # Generate recommendations based on the user query
        result = qa_chain({"query":query})
        
        return result['result']
  