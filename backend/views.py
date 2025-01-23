from django.shortcuts import render
from PyPDF2 import PdfReader
import re
from .constants import (
    tfidf_vectorizer_categorization,
    rf_classifier_categorization,
    tfidf_vectorizer_job_recommendation,
    rf_classifier_job_recommendation,
    education_keywords,
    skills_list,
)

# Clean resume
def cleanResume(txt):
    cleanText = re.sub("http\S+\s", " ", txt)
    cleanText = re.sub("RT|cc", " ", cleanText)
    cleanText = re.sub("#\S+\s", " ", cleanText)
    cleanText = re.sub("@\S+", "  ", cleanText)
    cleanText = re.sub(
        "[%s]" % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), " ", cleanText
    )
    cleanText = re.sub(r"[^\x00-\x7f]", " ", cleanText)
    cleanText = re.sub("\s+", " ", cleanText)
    return cleanText


# Prediction and Category Name
def predict_category(resume_text):
    resume_text = cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_categorization.transform([resume_text])
    predicted_category = rf_classifier_categorization.predict(resume_tfidf)[0]
    return predicted_category


# Prediction and Category Name
def job_recommendation(resume_text):
    resume_text = cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_job_recommendation.transform([resume_text])
    recommended_job = rf_classifier_job_recommendation.predict(resume_tfidf)[0]
    return recommended_job


def pdf_to_text(file):
    reader = PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text


def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number


def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email


def extract_skills_from_resume(text):
    # List of predefined skills

    skills = []

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return skills


def extract_education_from_resume(text):
    education = []

    # List of education keywords to match against

    for keyword in education_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        match = re.search(pattern, text)
        if match:
            education.append(match.group())

    return education


def extract_name_from_resume(text):
    name = None

    # Use regex pattern to find a potential name
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()

    return name
