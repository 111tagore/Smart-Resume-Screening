# ======================================================
# ML module for Smart Resume Screening System
# ======================================================

import re
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


nltk_data_dir = os.path.join(os.path.expanduser("~"), "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

for resource in ["punkt", "stopwords", "wordnet"]:
    try:
        if resource == "punkt":
            nltk.data.find("tokenizers/punkt")
        else:
            nltk.data.find(f"corpora/{resource}")
    except LookupError:
        nltk.download(resource, download_dir=nltk_data_dir, quiet=True)

# Initialize stopwords and lemmatizer
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


# -------------------------------------------------------
# Clean resume/job text
# -------------------------------------------------------
def clean_text(text: str) -> str:
    """
    Lowercase → remove unwanted characters → remove stopwords → lemmatize
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    tokens = nltk.word_tokenize(text)
    cleaned = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stop_words and len(word) > 2
    ]

    return " ".join(cleaned)


# -------------------------------------------------------
# Compute ML similarity score (0–10)
# -------------------------------------------------------
def score_resumes(resume_texts: list[str], job_description: str) -> list[float]:
    """
    Compute similarity scores between resumes and job description
    using TF-IDF and cosine similarity.
    """
    cleaned_resumes = [clean_text(t) for t in resume_texts]
    cleaned_job = clean_text(job_description)

    corpus = cleaned_resumes + [cleaned_job]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    resume_vectors = tfidf_matrix[:-1]
    job_vector = tfidf_matrix[-1]

    similarities = cosine_similarity(resume_vectors, job_vector.reshape(1, -1))
    scores = (similarities.flatten() * 10).round(2)
    return scores.tolist()


# -------------------------------------------------------
# Rank resumes by score
# -------------------------------------------------------
def rank_resumes(resume_texts: list[str], job_description: str, file_names: list[str] = None, top_n: int = None) -> list[dict]:
    """
    Rank resumes by similarity score with job description.
    Returns top N candidates if top_n is specified, else all.
    """
    scores = score_resumes(resume_texts, job_description)

    results = [
        {"resume": file_names[i] if file_names else f"Resume_{i+1}", "score": score}
        for i, score in enumerate(scores)
    ]

    results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)

    if top_n is not None:
        results_sorted = results_sorted[:top_n]

    return results_sorted
