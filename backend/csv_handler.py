
import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from utils import generate_forecast_plot

def answer_from_csv(query: str, selected_files: list[str] = [], plotting_intent: bool = False) -> dict:
    """Answers a question from a CSV file, with an option to generate a forecast plot."""
    data_dir = "/Users/dheeraj/Desktop/finalmp/data"
    
    if not selected_files:
        return {"error": "Please select a CSV file to query."}

    # Use the first selected CSV file
    csv_file_name = None
    for file in selected_files:
        if file.endswith('.csv'):
            csv_file_name = file
            break
    
    if not csv_file_name:
        return {"error": "No CSV file was selected."}

    file_path = os.path.join(data_dir, csv_file_name)

    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig', sep=',', engine='python')
    except Exception as e:
        return {"error": f"Error reading CSV file: {e}"}

    # --- Forecasting Logic ---
    if plotting_intent:
        print(f"--- Plotting intent detected for CSV. Attempting to generate forecast... ---")
        return generate_forecast_plot(df, csv_file_name)

    # --- Standard CSV Analysis Logic ---
    else:
        csv_content = df.to_string()
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=os.getenv("GEMINI_API_KEY"))
        prompt = f"""
        You are an expert business analyst. Your task is to answer the user's query based on the provided CSV data.

        CSV Data:
        {csv_content}

        Query: "{query}"

        Based on the CSV data, provide a concise and insightful answer to the query.
        """
        try:
            response = llm.invoke(prompt)
            return {"answer": response.content.strip()}
        except Exception as e:
            return {"error": f"Error during LLM analysis of CSV: {e}"}

