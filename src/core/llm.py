from langchain_ollama import ChatOllama
from src.config.config import CONFIG
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def initialize_llm():
    """Initialize LLM based on configuration."""
    provider = CONFIG["llm_provider"]
    
    if provider == "ollama":
        logger.info(f"Initializing Ollama LLM: {CONFIG['ollama_model']}")
        llm = ChatOllama(
            model=CONFIG["ollama_model"],
            base_url=CONFIG["ollama_base_url"],
            temperature=CONFIG["temperature"]
        )
        return llm
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")