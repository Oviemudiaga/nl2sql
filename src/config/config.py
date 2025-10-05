import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CONFIG = {
    # LLM Configuration
    "llm_provider": os.getenv("LLM_PROVIDER", "ollama"),
    "ollama_model": os.getenv("OLLAMA_MODEL", "llama3"),
    "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    
    # Database Configuration
    "database_path": os.getenv("DATABASE_PATH", "sample.db"),
    "database_uri": f"sqlite:///{os.getenv('DATABASE_PATH', 'sample.db')}",
    
    # ChromaDB Configuration
    "chromadb_path": os.getenv("CHROMADB_PATH", "./chromadb"),
    "chromadb_collection": "sql_schemas",
    "embedding_model": os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
    
    # Agent Configuration
    "max_iterations": 5,
    "verbose": True,
    "temperature": 0,
    
    # Schema Fallback (used if ChromaDB fails)
    "schema": """
CREATE TABLE airplanes (
    Airplane_id INT(10) PRIMARY KEY,
    Producer VARCHAR(20),
    Type VARCHAR(10)
);
    """
}