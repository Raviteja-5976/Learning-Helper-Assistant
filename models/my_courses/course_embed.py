from langchain_community.document_loaders import PyPDFLoader  # Import PDF loader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from groq import Groq
import os
from langchain.docstore.document import Document
import time
from models.config import GROQ_API_KEY_COURSE_EMBED

CHROMA_PATH = r"C:\Users\ravit\Desktop\Learning-Helper-Assistant\chroma"

def load_doc(file_path):
    # Use PyPDFLoader to load the file from the file path
    loader = PyPDFLoader(file_path)
    data = loader.load()
    return data

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=400
)

def summarize_chunk(chunk, max_tokens):
    client = Groq(api_key=GROQ_API_KEY_COURSE_EMBED)  # Make sure to provide your API key here
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": f"Summarize the content in less than 100 words: {chunk}"}],
        temperature=0.74,
        max_tokens=max_tokens,
        top_p=1,
        stream=False,
        stop=None,
    )
    summary = completion.choices[0].message.content
    return summary

def process_file(text, db_name):
    # Create a Document object from the text
    doc = Document(page_content=text)
    documents = text_splitter.split_documents([doc])

    summarized_documents = []
    requests_made = 0
    tokens_used = 0
    start_time = time.time()

    for doc in documents:
        chunk = doc.page_content
        estimated_input_tokens = len(chunk) // 4  # Approximate conversion: 1 token ≈ 4 characters
        max_tokens_per_request = 800  # Adjusted max_tokens per request
        estimated_tokens = estimated_input_tokens + max_tokens_per_request

        # Rate limiting for tokens per minute
        tokens_used += estimated_tokens
        elapsed_time = time.time() - start_time
        if tokens_used > 30000:
            sleep_time = 60 - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)
            tokens_used = 0
            start_time = time.time()

        # Rate limiting for requests per minute
        requests_made += 1
        if requests_made > 29:
            sleep_time = 60 - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)
            requests_made = 0
            start_time = time.time()

        summary = summarize_chunk(chunk, max_tokens_per_request)
        summarized_text = f"\n\nSummary: {summary}\ndata : {chunk}"
        summarized_doc = Document(page_content=summarized_text)
        summarized_documents.append(summarized_doc)

    # Set the path for the Chroma database
    CHROMA_PATH = os.path.join("chroma", db_name)

    # Create and persist the Chroma database
    Chroma.from_documents(
        summarized_documents,
        OllamaEmbeddings(model='nomic-embed-text'),
        persist_directory=CHROMA_PATH
    )


