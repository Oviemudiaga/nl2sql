from src.core.llm import initialize_llm
from src.core.database import create_sample_database, initialize_database
from src.core.schema_retrieval import initialize_vector_store
from src.tools.mcp_tools import initialize_mcp_tools
from src.agents.agent import initialize_agent, process_text_to_sql
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def main():
    """Main application entry point."""
    
    print("=" * 60)
    print("🚀 Text-to-SQL Application using MCP")
    print("=" * 60)
    
    # Step 1: Setup database
    logger.info("Setting up database...")
    create_sample_database()
    db = initialize_database()
    
    # Step 2: Initialize LLM
    logger.info("Initializing LLM...")
    llm = initialize_llm()
    
    # Step 3: Initialize vector store
    logger.info("Initializing ChromaDB...")
    vector_store = initialize_vector_store()
    
    # Step 4: Initialize MCP client
    logger.info("Initializing MCP tools...")
    mcp_client = initialize_mcp_tools(db, vector_store)
    
    # Step 5: Initialize agent
    logger.info("Initializing ReAct agent...")
    executor = initialize_agent(llm, db, mcp_client, vector_store)
    
    # Step 6: Test queries
    test_questions = [
        "How many unique airplane producers are there?",
        "List all commercial airplanes",
        "What types of airplanes does Boeing produce?",
        "Count total number of airplanes"
    ]
    
    print("\n" + "=" * 60)
    print("📊 Running Test Queries")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print("-" * 60)
        
        result = process_text_to_sql(executor, mcp_client, vector_store, question)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"🔍 SQL Query: {result.get('sql_query', 'N/A')}")
            print(f"✅ Result: {result.get('result', 'N/A')}")

if __name__ == "__main__":
    main()