# utils.py
import os
import re
from io import BytesIO
from PyPDF2 import PdfReader
import docx
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ensure NLTK data is downloaded (first run)
nltk_packages = ["punkt","stopwords","wordnet","omw-1.4"]
for pkg in nltk_packages:
    try:
        nltk.data.find(pkg)
    except:
        nltk.download(pkg)

STOPWORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def extract_text_from_pdf(file_path):
    text = []
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return "\n".join(fullText)

def extract_text(file_path, filename):
    ext = filename.split(".")[-1].lower()
    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext in ["docx","doc"]:
        return extract_text_from_docx(file_path)
    else:
        # fallback: read plain text
        with open(file_path, "r", encoding="utf8", errors="ignore") as f:
            return f.read()

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Remove emails, urls, special characters
    text = re.sub(r'\S+@\S+\.\S+', ' ', text)  # emails
    text = re.sub(r'http\S+|www\S+', ' ', text) # urls
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Tokenize
    tokens = nltk.word_tokenize(text)
    # Remove stopwords & lemmatize & filter short tokens
    tokens = [lemmatizer.lemmatize(tok) for tok in tokens if tok not in STOPWORDS and len(tok)>2]
    return " ".join(tokens)

def extract_keywords_from_jobrole(job_text, top_k=10):
    # Basic frequency-based extraction
    job_text = re.sub(r'[^a-z0-9\s]', ' ', job_text.lower())
    tokens = nltk.word_tokenize(job_text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in STOPWORDS and len(t)>2]
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t,0)+1
    sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [t[0] for t in sorted_tokens[:top_k]]
