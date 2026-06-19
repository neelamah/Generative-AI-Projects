#  rag

from  langchain_groq import ChatGroq
from langchain.chains  import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from src.config import Config

class RAGChainBuilder:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.model = ChatGroq(model=Config.RAG_MODEL, temperature=0.5)
        self.history_store ={}
    
    # fetch chat from set history
    def _get_history(self, session_id:str) -> BaseChatMessageHistory:
        if  session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]
    
    #build chain
    def build_chain(self):
         retriever = self.vector_store.as_retriever(search_kwargs={"k":3})
         
         #context prompt
         context_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the chat history and user question, rewrite it as a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])
         
         # query prompt
         qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You're an e-commerce bot answering product-related queries using reviews and titles.
                          Stick to context. Be concise and helpful.\n\nCONTEXT:\n{context}\n\nQUESTION: {input}"""),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])
         
         # it is for rewite user query. so it can understand follow-up questions using chat history.( taking about whome)
         history_aware_retriever = create_history_aware_retriever(
            self.model , retriever , context_prompt
        )
         
         # It is a Chain Take all retrieved documents and "stuff" them into the prompt context before calling the LLM.
         question_answer_chain = create_stuff_documents_chain(
             self.model, qa_prompt
         )

         # creates an end-to-end RAG chain by connecting the retriever (to fetch relevant documents) with the question-answer chain (to generate the final answer using those documents).
         rag_chain = create_retrieval_chain(
             history_aware_retriever, question_answer_chain
         )
         
         #It wraps the RAG chain with chat memory so previous conversations (chat_history) are automatically passed to the chain and new user/AI messages are saved.
         #adds conversation memory to your RAG chain by storing and retrieving chat history for each user session.
         return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
    