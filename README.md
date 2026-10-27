# Gastrointestinal and Urine Health Chatbot

A Streamlit-based conversational application that helps users explore general educational information about gastrointestinal and urinary health. The chatbot retrieves relevant passages from a supplied health-information PDF and uses an OpenAI language model to respond within the context of that source material.

> **Important:** This project is for general educational information only. It is not a diagnostic tool and must not replace advice, diagnosis, or treatment from a qualified healthcare professional. Users with concerning, severe, or persistent symptoms should seek professional medical care.

## Features

- Conversational question-and-answer interface built with Streamlit
- PDF text extraction with PyPDF2
- Text chunking for document retrieval
- OpenAI embeddings for semantic search
- FAISS vector store for efficient similarity retrieval
- Conversational memory for multi-turn chats
- Custom chat-message styling and avatars

## How It Works

1. The application reads the configured health-information PDF from `FeedDocs/`.
2. The PDF text is split into smaller chunks.
3. OpenAI embeddings are created for those chunks and stored in a FAISS vector store.
4. When a user submits a question, the app retrieves relevant information and sends it to a conversational retrieval chain.
5. The chatbot returns a context-aware response in the Streamlit interface.

## Technologies

- Python
- Streamlit
- LangChain
- OpenAI API
- FAISS
- PyPDF2
- python-dotenv

## Requirements

- Python 3.10 or later
- An OpenAI API key
- The dependency list from `requirements.txt`

## Setup

The application source currently lives on the `master` branch. Switch to that branch after cloning:

```bash
git clone https://github.com/Tarantula-Jeff/Gastrointestinal-and-Urine-health-chatbot.git
cd Gastrointestinal-and-Urine-health-chatbot
git checkout master
```

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Start the application:

```bash
streamlit run app.py
```

## Project Structure

```text
app.py              # Streamlit application and retrieval workflow
htmlTemplates.py    # Custom chat styling and message templates
FeedDocs/           # Source health-information PDF documents
IMG/                # Chat-avatar images
requirements.txt    # Python dependencies
```

## Privacy and Safety Notes

- Do not add real patient information, personal health records, or other sensitive data to the application or source documents.
- Keep API keys in `.env` or Streamlit secrets; never commit them to a public repository.
- Responses should be treated as informational and reviewed alongside reputable healthcare resources and professional advice.

## Author

Jeffrey Ackah
