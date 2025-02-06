import os
import sys
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from pathlib import Path

# Add project root to Python path
current_dir = Path(__file__).parent  # app/
project_root = current_dir.parent  # document-qa-rag/
sys.path.append(str(project_root))
from src.qa_builder import build_qa_system
from src.cache_manager import get_cache_path, get_file_hash
import traceback

load_dotenv()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "file_hash" not in st.session_state:
    st.session_state.file_hash = None

# Configure Streamlit
st.set_page_config(page_title="Multi-Doc Q&A", layout="wide")
st.title("📚 Multi-Document Q&A with Gemini")

# Sidebar: File upload
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDFs", type="pdf", accept_multiple_files=True
    )

    if st.button("Clear Chat History"):
        st.session_state.messages = []

# Process uploaded files
if uploaded_files:
    try:
        # Save files to data/ directory
        file_paths = []
        for file in uploaded_files:
            file_path = os.path.join("data", file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            file_paths.append(file_path)

        # Check cache
        current_hash = get_file_hash(file_paths)
        cache_path = get_cache_path(file_paths)

        if os.path.exists(cache_path) and current_hash == st.session_state.file_hash:
            # Load from cache
            st.session_state.vector_store = FAISS.load_local(
                cache_path,
                GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
                allow_dangerous_deserialization=True,
            )
        else:
            # Process and cache
            with st.spinner("Processing documents..."):
                st.session_state.vector_store = build_qa_system(file_paths)
                st.session_state.vector_store.save_local(cache_path)
                st.session_state.file_hash = current_hash

        st.success(f"Processed {len(uploaded_files)} documents!")

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.code(traceback.format_exc())

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize QA chain
if st.session_state.vector_store:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,  # Default creativity
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=st.session_state.vector_store.as_retriever(
                search_kwargs={"k": 5}  # Retrieve more chunks
            ),
            return_source_documents=True,
        )

        # Handle user input
        if prompt := st.chat_input("Ask about the documents"):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.spinner("Thinking..."):
                try:
                    response = qa_chain.invoke({"query": prompt})
                    answer = response["result"]
                    sources = list(
                        set(
                            f"Page {doc.metadata['page']+1}"  # Show human-readable pages
                            for doc in response["source_documents"]
                        )
                    )
                    answer += f"\n\n📚 Sources: {', '.join(sources)}"
                except Exception as e:
                    answer = f"Error generating response: {str(e)}"

            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)

    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
