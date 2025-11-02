
import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI

def answer_from_csv(query: str) -> str:
    """Answers a question from a CSV file."""

    # Find the first CSV file in the data directory
    data_dir = "/Users/dheeraj/Desktop/finalmp/data"
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not csv_files:
        return "No CSV file found in the data directory."
    
    csv_path = os.path.join(data_dir, csv_files[0])

    # Read the CSV file
    try:
        df = pd.read_csv(csv_path)
        csv_content = df.to_string()
    except Exception as e:
        return f"Error reading CSV file: {e}"

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    You are a data analyst. Your task is to answer the user's query based on the provided CSV data.

    CSV Data:
    """
    {csv_content}
    """

    Query: "{query}"

    Based on the CSV data, provide a concise answer to the query.
    """

    response = llm.invoke(prompt)

    return response.content.strip()

