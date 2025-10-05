from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools.sql_database.tool import (
    QuerySQLDataBaseTool,
    ListSQLDatabaseTool
)
from langchain_core.prompts import PromptTemplate
from src.tools.mcp_tools import SchemaRetrievalTool
from src.config.config import CONFIG
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

SQL_PROMPT = PromptTemplate.from_template("""
You are an expert SQL assistant. Generate and execute SQL queries to answer questions.

Your goal:
1. Generate a syntactically correct SQL query
2. Execute it using sql_db_query tool
3. Verify the result makes sense

If the query fails, analyze the error and retry.

Question: {question}
Schema: {schema}

Available tools:
{tools}

Tool names: {tool_names}

Process:
Thought: [Your reasoning]
Action: sql_db_query
Action Input: [SQL query]
Observation: [Result from tool]
Thought: [Verify result]
Final Answer: [The result]

If asked for only the query, return:
Final Answer: [SQL query only]

{agent_scratchpad}
""")

def initialize_agent(llm, db, mcp_client, vector_store=None):
    """Initialize LangChain ReAct agent."""
    
    # Create tools
    query_tool = QuerySQLDataBaseTool(db=db)
    list_tables_tool = ListSQLDatabaseTool(db=db)
    schema_tool = SchemaRetrievalTool(
        mcp_client=mcp_client,
        vector_store=vector_store
    )
    
    # Create agent
    agent = create_react_agent(
        llm=llm,
        tools=[query_tool, list_tables_tool, schema_tool],
        prompt=SQL_PROMPT
    )
    
    # Create executor
    executor = AgentExecutor(
        agent=agent,
        tools=[query_tool, list_tables_tool, schema_tool],
        verbose=CONFIG["verbose"],
        max_iterations=CONFIG["max_iterations"],
        handle_parsing_errors=True
    )
    
    logger.info("✅ ReAct agent initialized")
    return executor

def process_text_to_sql(executor, mcp_client, vector_store, question: str) -> dict:
    """Process natural language query to SQL."""
    try:
        # Retrieve schema
        schema = mcp_client.call_tool(
            "retrieve_schema",
            {"query": question, "vector_store": vector_store}
        )
        
        # Execute agent
        result = executor.invoke({
            "question": question,
            "schema": schema
        })
        
        output = result.get("output", "No result")
        
        # Extract query and result
        query = None
        query_result = output
        
        if "SELECT" in output.upper():
            for step in result.get("intermediate_steps", []):
                if step[0].tool == "sql_db_query":
                    query = step[0].tool_input
                    query_result = step[1] if step[1] else output
                    break
        
        return {
            "question": question,
            "sql_query": query,
            "result": query_result
        }
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return {"question": question, "error": str(e)}