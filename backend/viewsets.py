# classnest_Base/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .views import *


def pred(request):
    context = {}
    if request.method == "POST" and request.FILES:
        # Assuming 'resume_file' is the name of the file input field
        file = request.FILES["resume"]
        filename = file.name
        if filename.endswith(".pdf"):
            text = pdf_to_text(file)
        elif filename.endswith(".txt"):
            text = file.read().decode("utf-8")
        else:
            return render(
                request,
                "resume.html",
                message="Invalid file format. Please upload a PDF or TXT file.",
            )
        context = {
            "predicted_category": predict_category(text),
            "recommended_job": job_recommendation(text),
            "phone": extract_contact_number_from_resume(text),
            "name": extract_name_from_resume(text),
            "email": extract_email_from_resume(text),
            "extracted_skills": extract_skills_from_resume(text),
            "extracted_education": extract_education_from_resume(text),
        }

    return render(request, "resume.html", context=context)


def resume(request):
    # Provide a simple UI to upload a resume
    print("inside resume class")
    return render(request, "resume.html")
