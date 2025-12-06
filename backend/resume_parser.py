import os
import re
import pdfplumber
import docx2txt
import spacy

# Load spacy model once
nlp = spacy.load("en_core_web_sm")


# Read text from different resume formats
def extract_text(path):
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".pdf":
        text = ""
        with pdfplumber.open(path) as pdf:
            for pg in pdf.pages:
                t = pg.extract_text()
                if t:
                    text += t + "\n"
        return text

    if ext == ".docx":
        return docx2txt.process(path)

    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    raise Exception("Unsupported file format")


# Basic regex helpers
def get_email(text):
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return emails[0] if emails else None


def get_phone(text):
    phones = re.findall(r"\+?\d[\d\s\-]{8,15}", text)
    return phones[0] if phones else None


# Try to get name from the first line
def get_name(text):
    first_line = text.split("\n")[0]
    doc = nlp(first_line)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


# Simple keyword-based skill extractor
def get_skills(text):
    skills_list = [
        "python", "java", "c++", "javascript", "react", "node",
        "machine learning", "deep learning", "ml", "nlp",
        "sql", "mongodb", "html", "css", "django",
        "aws", "docker", "api", "flutter"
    ]

    text = text.lower()
    found = [s for s in skills_list if s in text]
    return list(set(found))


# Check for experience duration
def get_experience(text):
    pattern = r"(\d+\.?\d*)\s+(years?|yrs?)"
    match = re.findall(pattern, text.lower())
    if match:
        return match[0][0] + " years"
    return None


# Main function to call
def parse_resume(path):
    text = extract_text(path)

    return {
        "name": get_name(text),
        "email": get_email(text),
        "phone": get_phone(text),
        "skills": get_skills(text),
        "experience": get_experience(text),
        "raw_text": text
    }


# Local test
if __name__ == "__main__":
    resume = "sample_resume.pdf"
    out = parse_resume(resume)
    for k, v in out.items():
        print(f"{k}: {v}")
