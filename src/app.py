import threading
from logger import Logger

from flask import Flask, request, jsonify
from config import INDEX_PASSWORD
from store import initialize_store
from qa_chain import initialize_qa_chain
from indexer import load_data
from langchain_openai import OpenAIEmbeddings
from config import CONNECTION_STRING, OPENAI_EMBEDDINGS_MODEL
from langchain_postgres import PGEngine

app = Flask(__name__)

Logger.configure()
logger = Logger.get(__name__)
logger.info("Starting RAG API")

engine = None
vector_store = None
embeddings = None
qa_chain = None

@app.route('/index', methods=['POST'])
def index_route():
    data = request.get_json(silent=True) or {}
    if data.get('password') != INDEX_PASSWORD:
        return jsonify({'error': 'Unauthorized'}), 401
    threading.Thread(target=load_data, args=(engine, vector_store, embeddings, initialize_store), daemon=True).start()
    return jsonify({'status': 'Indexing started'}), 202

@app.route('/ask', methods=['POST'])
def ask_route():
    if vector_store is None:
        return jsonify({'error': 'Not indexed yet'}), 503
    data = request.get_json(silent=True) or {}
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    qa_chain = initialize_qa_chain(vector_store)
    answer = qa_chain.invoke({"input": question})
    return jsonify({'answer': answer.get('answer', '') if isinstance(answer, dict) else str(answer)})

@app.route('/health', methods=['GET'])
def health_route():
    status = 'ready' if qa_chain else 'initializing'
    return jsonify({'status':status}), (200 if qa_chain else 503)

if __name__ == '__main__':
    try:
        engine = PGEngine.from_connection_string(url=CONNECTION_STRING)
        embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDINGS_MODEL)
        vector_store = initialize_store(engine, embeddings) or load_data(engine, vector_store, embeddings, initialize_store)
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
    logger.info("Starting RAG API")
    app.run(host='0.0.0.0', port=8080, debug=True)