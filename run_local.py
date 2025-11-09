#!/usr/bin/env python3
import sqlite3
import os
from app.process_pdfs import extract_text_from_pdf, clean_text, get_keyword_frequency

# Use SQLite for local testing
DB_PATH = "pdf_analysis.db"

def setup_sqlite_db():
    """Create SQLite database and table for local testing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keyword_frequency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pdf_name TEXT NOT NULL,
            keyword TEXT NOT NULL,
            frequency INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(pdf_name, keyword)
        )
    ''')
    conn.commit()
    return conn

def store_results_sqlite(conn, pdf_name, keywords):
    """Store results in SQLite database."""
    cursor = conn.cursor()
    for keyword, frequency in keywords:
        cursor.execute('''
            INSERT OR REPLACE INTO keyword_frequency (pdf_name, keyword, frequency)
            VALUES (?, ?, ?)
        ''', (pdf_name, keyword, frequency))
    conn.commit()
    print(f"Successfully stored keywords for {pdf_name}")

def main():
    """Run PDF processing with SQLite for local testing."""
    print("Starting PDF processing pipeline (local SQLite mode)...")
    
    # Create sample PDF content for testing
    sample_dir = "data"
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
    
    # Check for PDF files
    pdf_files = [f for f in os.listdir(sample_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in data/ directory.")
        print("Creating sample text for demonstration...")
        
        # Process sample text instead
        sample_text = """
        Machine learning is a subset of artificial intelligence that focuses on algorithms 
        and statistical models. Data science involves extracting insights from data using 
        various techniques including machine learning, statistics, and data visualization.
        Python is a popular programming language for data analysis and machine learning.
        """
        
        conn = setup_sqlite_db()
        cleaned_tokens = clean_text(sample_text)
        keywords = get_keyword_frequency(cleaned_tokens)
        store_results_sqlite(conn, "sample_text.txt", keywords)
        
        # Display results
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM keyword_frequency")
        results = cursor.fetchall()
        
        print("\nKeyword Analysis Results:")
        for row in results:
            print(f"File: {row[1]}, Keyword: {row[2]}, Frequency: {row[3]}")
        
        conn.close()
        return
    
    # Process actual PDF files
    conn = setup_sqlite_db()
    
    for filename in pdf_files:
        pdf_path = os.path.join(sample_dir, filename)
        print(f"Processing {filename}...")
        
        raw_text = extract_text_from_pdf(pdf_path)
        if raw_text:
            cleaned_tokens = clean_text(raw_text)
            keywords = get_keyword_frequency(cleaned_tokens)
            store_results_sqlite(conn, filename, keywords)
    
    conn.close()
    print("Pipeline finished.")

if __name__ == "__main__":
    main()