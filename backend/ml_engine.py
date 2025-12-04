# ml_engine.py
import os
import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_scores(resume_texts, job_role_text):
    corpus = [job_role_text] + resume_texts
    vectorizer = TfidfVectorizer(max_features=5000)
    tfidf = vectorizer.fit_transform(corpus)
    job_vec = tfidf[0]
    resume_vecs = tfidf[1:]
    sims = cosine_similarity(resume_vecs, job_vec).flatten()
    max_sim = sims.max() if sims.size>0 else 1.0
    scores = []
    for s in sims:
        if math.isclose(max_sim, 0.0):
            scaled = 0.0
        else:
            scaled = (s / max_sim) * 10.0
        scores.append(round(float(scaled), 2))
    return scores
