# Document QA System with Streamlit & Gemini

An interactive document question-answering system built with Streamlit and Google's Gemini API. Upload documents and ask questions through a user-friendly web interface.

## Features

- Web-based interface using Streamlit
- Real-time document processing and Q&A
- Drag-and-drop document upload
- Interactive chat-like interface
- Powered by Google Gemini API
- Document history management
- Response highlighting and formatting

## Prerequisites

- Python 3.8+
- Google Cloud API key
- Streamlit account (for deployment)
- Required packages listed in `requirements.txt`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/document-qa-rag.git
cd document-qa-rag
```

2. Set up virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

1. Set up your credentials:

```bash
export GOOGLE_API_KEY='your-api-key'
```

2. Run the Streamlit app:

```bash
streamlit run src/app.py
```

3. Open your browser and navigate to `http://localhost:8501`

## Project Structure

```
document-qa-rag/
├── src/
│   ├── app.py            # Main Streamlit application
│   ├── processor.py      # Document processing logic
│   ├── qa_chain.py      # Q&A chain with Gemini
│   └── utils/
│       ├── gemini.py     # Gemini API integration
│       └── ui.py         # UI components
├── pages/               # Additional Streamlit pages
├── static/             # Static assets
└── config/             # Configuration files
```

## Using the Application

1. Launch the application
2. Upload your documents using the file uploader
3. Wait for processing to complete
4. Type your questions in the chat input
5. View responses with highlighted relevant sections

## Configuration Options

```bash
# .env file configuration
GOOGLE_API_KEY=your-api-key
STREAMLIT_THEME=light/dark
MAX_TOKENS=1000
TEMPERATURE=0.7
```

## Deployment

Deploy to Streamlit Cloud:

1. Push to GitHub
2. Connect your repository to Streamlit Cloud
3. Configure environment variables
4. Deploy
