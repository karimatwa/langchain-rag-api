from langchain_postgres import PGVectorStore
from logger import Logger
logger = Logger.get(__name__)

def initialize_store(engine, embeddings):
    try:
        vector_store = PGVectorStore.create_sync(
            engine=engine,
            table_name='documents',
            embedding_service=embeddings
        )
        logger.info('💾 Vector Store initialized')
        return vector_store
    except Exception:
        logger.error("💾 Vector Store initialization failed: Table documents does not exist")
        return None