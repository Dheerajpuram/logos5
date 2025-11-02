import os
from langchain_google_genai import ChatGoogleGenerativeAI

def route_query(query: str) -> str:
    """Classifies the user's query and returns the data source type."""

    print("--- Routing query... ---")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    You are an expert query router. Your task is to classify the user's query and determine the most appropriate data source. You need to be smart about this. A query might sound like it's for a database, but it could be a question about a recently uploaded document.

    The available data sources are: SQL, RAG, CSV.

    - Use SQL for queries that involve calculations, aggregations, or questions about structured data in a database.
      Examples: 'What are the total sales for the last quarter?', 'Show me the top 5 selling products.', 'How many users are there?'

    - Use RAG for queries about the content of uploaded documents (like PDFs, Word documents, or Excel files). If the query is asking to summarize, analyze, or find specific information within a document, use RAG. **Prioritize RAG for document-specific questions, especially if the query mentions summarizing, analyzing, or extracting information from the document itself.**
      Examples: 'What is the company's policy on remote work?', 'Summarize the key findings of the research paper.', 'What were the sales and marketing expenses last year?'

    - Use CSV for queries on simple tabular data from a CSV file. **If a CSV file is selected and the query is about analyzing, forecasting, or extracting data from that file, prioritize CSV.**
      Examples: 'What is the price of product X?', 'List all products in the category Y.', 'Forecast sales from this CSV.'

    Query: "{query}"

    Based on the query, which data source should be used? Respond with only one word: SQL, RAG, or CSV.
    """

    print("--- Calling Gemini API for routing... ---")
    try:
        response = llm.invoke(prompt)
        print(f"--- Gemini API response: {response.content.strip()} ---")
        return response.content.strip()
    except Exception as e:
        print(f"--- Error calling Gemini API: {e} ---")
        return "Unknown"