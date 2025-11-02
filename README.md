
# Multi-Source AI Copilot

This project is a conversational business intelligence agent that can query and analyze data from multiple sources: SQL databases, PDFs, and CSV files.

## Features

- **Intelligent Query Routing**: Automatically determines the best data source for a given query.
- **Multi-Modal Responses**: Generates both text-based answers and data visualizations.
- **Pluggable Data Sources**: Easily extendable to include more data sources.
- **Web-based Interface**: Simple and intuitive UI for interacting with the copilot.

## Project Structure

- `backend/`: FastAPI backend containing the core logic.
- `frontend/`: React frontend for the user interface.
- `data/`: Directory for storing PDF and CSV files.
- `docs/`: Project documentation.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install backend dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Install frontend dependencies:**
    ```bash
    cd frontend
    npm install
    cd ..
    ```

4.  **Set up environment variables:**
    - Create a `.env` file in the `backend` directory: `backend/.env`
    - Add your Gemini API key to the `.env` file:
      ```
      GEMINI_API_KEY="YOUR_API_KEY"
      ```

5.  **Set up the database:**
    - The SQL handler is configured to use the AdventureWorks sample database.
    - You need to have a running SQL Server instance with the AdventureWorks database restored.
    - Update the database connection details in `backend/sql_handler.py`.

## Running the Application

1.  **Start the backend server:**
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

2.  **Start the frontend server:**
    ```bash
    cd frontend
    npm start
    ```
    The frontend will be running at `http://localhost:3000`.

3.  **Open your browser** and navigate to `http://localhost:3000` to use the copilot.

## How to Use

1.  **Upload Files**: Use the file upload section to upload PDF or CSV files to the `data` directory.
2.  **Ask Questions**: Use the prompt box to ask questions in natural language.
    - For questions about the uploaded CSV file, the copilot will use the CSV handler.
    - For questions about the uploaded PDF files, the copilot will use the RAG handler.
    - For questions about the AdventureWorks database, the copilot will use the SQL handler.

# logos
