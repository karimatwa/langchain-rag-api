# config.py
from dotenv import load_dotenv
import os
from logger import Logger
logger = Logger.get(__name__)

# Load environment variables
load_dotenv('.env', override=True)

# Application settings
BASE_URL       = os.getenv('BASE_URL')
INDEX_PASSWORD = os.getenv('INDEX_PASSWORD')
USER_AGENT     = os.getenv('USER_AGENT')
SYSTEM_PROMPT  = os.getenv('SYSTEM_PROMPT')

# OpenAI settings
OPENAI_EMBEDDINGS_MODEL = os.getenv('OPENAI_EMBEDDINGS_MODEL')
OPENAI_CHAT_MODEL = os.getenv('OPENAI_CHAT_MODEL')
VECTOR_SIZE = os.getenv('VECTOR_SIZE')

# Postgres connection
POSTGRES_USER     = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST     = os.getenv('POSTGRES_HOST')
POSTGRES_PORT     = os.getenv('POSTGRES_PORT')
POSTGRES_DB       = os.getenv('POSTGRES_DB')
CONNECTION_STRING = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}"
    f":{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Validate required settings
required = [BASE_URL, INDEX_PASSWORD, OPENAI_EMBEDDINGS_MODEL, OPENAI_CHAT_MODEL, VECTOR_SIZE, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB]
if not all(required):
    raise RuntimeError('Missing environment variable')

logger.info('🔐 All required environment variables are set')