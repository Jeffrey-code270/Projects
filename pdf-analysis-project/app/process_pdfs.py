# app/process_pdfs.py
import  nltk
import os
import fitz  # PyMuPDF
import psycopg2
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
PDF_DIRECTORY = os.getenv("PDF_DIRECTORY", "data")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
TOP_N_KEYWORDS = 10 # Number of top keywords to store

# --- Text Processing ---
def clean_text(text):
    """Cleans raw text by lowercasing, removing non-alphanumeric characters and stopwords."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text) # Keep only letters and spaces
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    return cleaned_tokens

def get_keyword_frequency(tokens):
    """Calculates the frequency of the top N keywords."""
    return Counter(tokens).most_common(TOP_N_KEYWORDS)

# --- PDF Processing ---
def extract_text_from_pdf(pdf_path):
    """Extracts all text from a given PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

# --- Database Interaction ---
def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def store_results(conn, pdf_name, keywords):
    """Stores the PDF name and its keyword frequencies in the database."""
    with conn.cursor() as cur:
        for keyword, frequency in keywords:
            # Use ON CONFLICT to update frequency if the pdf/keyword pair already exists
            cur.execute(
                """
                INSERT INTO keyword_frequency (pdf_name, keyword, frequency)
                VALUES (%s, %s, %s)
                ON CONFLICT (pdf_name, keyword)
                DO UPDATE SET frequency = EXCLUDED.frequency;
                """,
                (pdf_name, keyword, frequency)
            )
    conn.commit()
    print(f"Successfully stored keywords for {pdf_name}")


# --- Main Execution ---
def main():
    """Main function to orchestrate the PDF processing pipeline."""
    print("Starting document processing pipeline...")
    conn = get_db_connection()

    for filename in os.listdir(PDF_DIRECTORY):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIRECTORY, filename)
            print(f"Processing {filename}...")

            raw_text = extract_text_from_pdf(pdf_path)
            if raw_text:
                cleaned_tokens = clean_text(raw_text)
                keywords = get_keyword_frequency(cleaned_tokens)
                store_results(conn, filename, keywords)

    conn.close()
    print("Pipeline finished.")

if __name__ == "__main__":
    main()