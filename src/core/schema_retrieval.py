import chromadb
from langchain_ollama import OllamaEmbeddings
from src.config.config import CONFIG
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def initialize_vector_store():
    """Initialize ChromaDB vector store for schema retrieval."""
    try:
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=CONFIG["chromadb_path"])
        
        # Get or create collection
        collection = client.get_or_create_collection(
            name=CONFIG["chromadb_collection"]
        )
        
        # Add schema to collection if empty
        if collection.count() == 0:
            schema_docs = [
                {
                    "id": "airplanes_schema",
                    "text": CONFIG["schema"],
                    "metadata": {"table": "airplanes"}
                }
            ]
            
            # Use Ollama embeddings
            embeddings_model = OllamaEmbeddings(
                model=CONFIG["embedding_model"],
                base_url=CONFIG["ollama_base_url"]
            )
            
            for doc in schema_docs:
                embedding = embeddings_model.embed_query(doc["text"])
                collection.add(
                    ids=[doc["id"]],
                    embeddings=[embedding],
                    documents=[doc["text"]],
                    metadatas=[doc["metadata"]]
                )
            
            logger.info(f"Added {len(schema_docs)} schemas to ChromaDB")
        
        logger.info(f"ChromaDB initialized with {collection.count()} schemas")
        return collection
    
    except Exception as e:
        logger.error(f"Error initializing ChromaDB: {e}")
        return None

def retrieve_schema(vector_store, query: str, k: int = 3) -> str:
    """Retrieve relevant schema from ChromaDB."""
    if vector_store is None:
        logger.warning("Using fallback schema from config")
        return CONFIG["schema"]
    
    try:
        # Use Ollama embeddings for query
        embeddings_model = OllamaEmbeddings(
            model=CONFIG["embedding_model"],
            base_url=CONFIG["ollama_base_url"]
        )
        query_embedding = embeddings_model.embed_query(query)
        
        # Query vector store
        results = vector_store.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        if results and 'documents' in results and results['documents']:
            schemas = results['documents'][0]
            combined_schema = "\n\n".join(schemas)
            logger.info(f"Retrieved {len(schemas)} relevant schemas")
            return combined_schema
        
        return CONFIG["schema"]
    
    except Exception as e:
        logger.error(f"Error retrieving schema: {e}")
        return CONFIG["schema"]