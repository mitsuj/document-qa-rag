from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()


def build_qa_system(file_paths: list):
    """Process multiple PDFs with standard parameters"""
    all_chunks = []

    for path in file_paths:
        try:
            loader = PyPDFLoader(path)
            pages = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,  # Default chunk size
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""],
            )
            chunks = text_splitter.split_documents(pages)
            all_chunks.extend(chunks)
        except Exception as e:
            raise RuntimeError(f"Error processing {path}: {str(e)}")

    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        return FAISS.from_documents(all_chunks, embeddings)
    except Exception as e:
        raise RuntimeError(f"Embedding error: {str(e)}")
