import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer
from loguru import logger

# Load environment variables
load_dotenv()

# ================================
# ENV VARIABLES
# ================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY not found in environment variables")

# ================================
# LLM CONFIGURATION
# ================================

def get_llm(model_name: str = "llama-3.1-8b-instant"):
    """
    Returns Groq LLM instance
    """
    try:
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=model_name,
            temperature=0.3,
            max_tokens=300
        )
        return llm
    except Exception as e:
        logger.error(f"LLM initialization failed: {e}")
        raise

# ================================
# EMBEDDING MODEL
# ================================

def get_embedding_model():
    """
    Load sentence transformer model
    """
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model
    except Exception as e:
        logger.error(f"Embedding model loading failed: {e}")
        raise

# ================================
# VECTOR DB PATH
# ================================

VECTOR_DB_PATH = "data/vector_store"

# ================================
# DATABASE PATH
# ================================

DATABASE_URL = "sqlite:///./data/app.db"

# ================================
# LOGGING CONFIG
# ================================

logger.add(
    "data/app.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO"
)