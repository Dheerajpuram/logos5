
import os
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from security import mask_pii
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent

def answer_from_sql(query: str) -> list:
    """Answers a question from a SQL database."""

    # --- DATABASE CONNECTION (PLACEHOLDERS) ---
    # Replace with your actual database credentials
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT", "5432") # Default PostgreSQL port
    db_name = os.getenv("POSTGRES_DB")

    connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    try:
        engine = create_engine(connection_string)
        db = SQLDatabase(engine)
    except Exception as e:
        return [{"error": f"Error connecting to the database: {e}"}]

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=os.getenv("GEMINI_API_KEY"))

    try:
        agent_executor = create_sql_agent(
            llm, 
            db=db, 
            agent_type="zero-shot-react-description", 
            verbose=True, 
            handle_parsing_errors=True,
            prefix="""You are an expert business analyst. You have access to a SQL database. 
Your task is to answer the user's query by generating and executing SQL queries. 
When appropriate, provide insights and suggestions based on the query results."""
        )
        result = agent_executor.run(query)
        result = mask_pii(str(result))
    except StopIteration:
        return [{"error": "The SQL agent could not complete the query. This may be because the query is out of scope for the database."}]
    except Exception as e:
        return [{"error": f"Error executing SQL query: {e}"}]

    # The result from the agent is a string. We need to parse it.
    # This is a simple parsing logic and might need to be improved.
    try:
        # Assuming the result is a list of tuples in a string format
        parsed_result = eval(result)
        if isinstance(parsed_result, list) and all(isinstance(item, tuple) and len(item) == 2 for item in parsed_result):
            return [{"label": item[0], "value": item[1]} for item in parsed_result]
        else:
            # If parsing fails, return the raw string result
            return [{"label": "Result", "value": result}]
    except:
        return [{"label": "Result", "value": result}]

