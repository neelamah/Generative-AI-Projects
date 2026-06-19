from flask import render_template,Flask,request,Response
from prometheus_client import Counter,generate_latest
from src.data_ingestion import DataIngestor
from src.rag_chain import RAGChainBuilder

from dotenv import load_dotenv
load_dotenv()

REQUEST_COUNT = Counter("http_requests_total" , "Total HTTP Request")

def create_app():

    app = Flask(__name__)

    #creates the vector database
    #DataIngestor handles document ingestion. Load Documents->Split into Chunks->Create Embeddings ->Store in Vector Database ->Return Vector Store
    #load_existing=True means: -> If vector DB already exists → load existing embeddings, Do not recreate embeddings again
    #alling DataIngestor py file to create vsctore
    vector_store = DataIngestor().ingest(load_existing=True)
    
    #builds the complete RAG pipeline using that vector store.
    # calling RAGChainBuilder py file  RAGChainBuilder class to initilaise and calling method of that class to create rag chain.
    rag_chain = RAGChainBuilder(vector_store).build_chain()

    @app.route("/")
    def index():
        REQUEST_COUNT.inc()
        return render_template("index.html")
    
    @app.route("/get" , methods=["POST"])
    def get_response():

        user_input = request.form["msg"]

        reponse = rag_chain.invoke(
            {"input" : user_input},
            config={"configurable" : {"session_id" : "user-session"}}
        )["answer"]

        return reponse
    
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")
    
    return app

if __name__=="__main__":
    app = create_app()
    app.run(host="0.0.0.0",port=5001,debug=True)