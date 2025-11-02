
import os
from PyPDF2 import PdfReader
import docx
import openpyxl
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

def answer_from_rag(query: str, selected_files: list[str] = []) -> str:
    """Answers a question from documents in the data directory using RAG."""

    data_dir = "/Users/dheeraj/Desktop/finalmp/data"
    if selected_files:
        files = selected_files
    else:
        files = [f for f in os.listdir(data_dir) if f.endswith(('.pdf', '.docx', '.xlsx'))]
    
    if not files:
        return "No supported files (.pdf, .docx, .xlsx) found in the data directory or selected."

    raw_text = ''
    for file in files:
        file_path = os.path.join(data_dir, file)
        print(f"--- Processing file: {file} ---")
        try:
            if file.endswith('.pdf'):
                reader = PdfReader(file_path)
                for page in reader.pages:
                    raw_text += page.extract_text()
            elif file.endswith('.docx'):
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    raw_text += para.text
            elif file.endswith('.xlsx'):
                workbook = openpyxl.load_workbook(file_path)
                for sheet_name in workbook.sheetnames:
                    sheet = workbook[sheet_name]
                    for row in sheet.iter_rows():
                        for cell in row:
                            if cell.value:
                                raw_text += str(cell.value) + ' '
                        raw_text += '\n'
        except Exception as e:
            return f"Error reading file {file}: {e}"

    print(f"--- Raw text length: {len(raw_text)} ---")
    if not raw_text:
        return "No text could be extracted from the supported files."

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    texts = text_splitter.split_text(raw_text)
    print(f"--- Number of text chunks: {len(texts)} ---")

    # Create embeddings and vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GEMINI_API_KEY"))
    try:
        vectorstore = FAISS.from_texts(texts, embeddings)
        print("--- Vector store created successfully ---")

        # Retrieve relevant chunks
        retriever = vectorstore.as_retriever()
        docs = retriever.get_relevant_documents(query)

    except Exception as e:
        return f"Error creating vector store or retrieving documents: {e}"

    # Generate answer
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=os.getenv("GEMINI_API_KEY"))

    context = ' '.join([doc.page_content for doc in docs])
    prompt = f"""
    You are an expert business analyst. Your task is to analyze the provided context from documents and answer the user's query. When appropriate, provide insights, suggestions, and forecasts based on the data. If the documents do not contain enough information to make a forecast or suggestion, explain what information is missing.

    Context:
    {context}

    Query: "{query}"

    Based on the context, provide a concise and insightful answer to the query.
    """

    response = llm.invoke(prompt)

    return response.content.strip()

