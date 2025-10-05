from langchain_core.tools import BaseTool
from pydantic import Field
from src.config.config import CONFIG
from src.core import schema_retrieval
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def execute_sql_query(query: str, db) -> str:
    """Execute SQL query and return results."""
    try:
        result = db.run(query)
        logger.info(f"Query executed successfully: {query}")
        return str(result)
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        logger.error(f"Query execution failed: {error_msg}")
        return error_msg

def list_tables(db) -> str:
    """List all tables in the database."""
    try:
        tables = db.get_usable_table_names()
        logger.info(f"Tables listed: {tables}")
        return str(tables)
    except Exception as e:
        return f"Error: {str(e)}"

def retrieve_schema_tool(query: str, vector_store) -> str:
    """Retrieve relevant schema from ChromaDB."""
    if vector_store is None:
        logger.info("Using fallback schema from CONFIG")
        return CONFIG["schema"]
    
    return schema_retrieval.retrieve_schema(vector_store, query)

class MCPClient:
    """Mock MCP client to dispatch tool calls."""
    
    def call_tool(self, tool_name: str, args: dict):
        """Route tool calls to appropriate functions."""
        if tool_name == "execute_sql_query":
            return execute_sql_query(args["query"], args["db"])
        elif tool_name == "list_tables":
            return list_tables(args["db"])
        elif tool_name == "retrieve_schema":
            return retrieve_schema_tool(args["query"], args.get("vector_store"))
        
        raise ValueError(f"Unknown tool: {tool_name}")

def initialize_mcp_tools(db, vector_store):
    """Initialize MCP client."""
    return MCPClient()

class SchemaRetrievalTool(BaseTool):
    """LangChain-compatible tool for schema retrieval."""
    
    name: str = "schema_retrieval"
    description: str = "Retrieve relevant database schema for a given query."
    mcp_client: object = Field(description="MCP client for schema retrieval")
    vector_store: object = Field(default=None, description="ChromaDB vector store")
    
    def _run(self, query: str) -> str:
        """Execute schema retrieval."""
        return self.mcp_client.call_tool(
            "retrieve_schema",
            {"query": query, "vector_store": self.vector_store}
        )
    
    async def _arun(self, query: str) -> str:
        """Async execution."""
        return self._run(query)