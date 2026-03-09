# AI Resume Screening System

An AI-powered web application that analyzes resumes, extracts candidate information, predicts suitable job roles, and assists recruiters in screening candidates efficiently.

## Features

* Upload and analyze resumes (PDF format)
* Extract candidate details (name, email, phone, links)
* Detect skills from resume text
* Predict top job roles using a Machine Learning model
* Calculate ATS (Applicant Tracking System) score
* Generate a candidate report (PDF)
* Send accept/reject email notifications automatically

## Tech Stack

* **Python**
* **Flask**
* **scikit-learn**
* **PyPDF2**
* **PyMuPDF (fitz)**
* **NumPy**
* **ReportLab**
* **SMTP (Gmail)**

## Installation

Clone the repository

```
git clone https://github.com/yourusername/resume-screening-system.git
cd resume-screening-system
```

Install dependencies

```
pip install -r requirements.txt
```

Create a `.env` file

```
EMAIL_PASSWORD=your_gmail_app_password
```

Run the application

```
python app.py
```

Open in browser

```
http://localhost:10000
```

## Usage

1. Upload a resume (PDF).
2. The system extracts skills and candidate details.
3. It predicts suitable job roles and calculates ATS score.
4. Recruiters can accept or reject the candidate and send an email notification.

## Author

Avin Goel
