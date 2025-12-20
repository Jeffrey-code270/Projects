import nltk

def download_nltk_data():
    """Download required NLTK data."""
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')

if __name__ == "__main__":
    download_nltk_data()
    print("NLTK data downloaded successfully!")