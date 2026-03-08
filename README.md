AI Recruitment Assistant 🤖📄

An AI-powered Resume Screening and Applicant Tracking System (ATS) built with Python, Machine Learning, and Flask.
The system analyzes resumes, extracts candidate information, predicts suitable job roles, and assists recruiters in shortlisting candidates efficiently.

Features 🚀
Resume Parsing

Extracts Name, Email, Phone, LinkedIn, GitHub, and LeetCode

Detects hidden hyperlinks like mailto, LinkedIn profile links, etc.

Skill Detection

Automatically detects technical skills such as:

Python
Java
C++
Machine Learning
SQL
AWS
Docker
TensorFlow
Pandas
NumPy
Job Role Prediction

Uses a Machine Learning model (TF-IDF + classifier) to predict the most suitable role for the candidate.

Example roles:

Data Scientist

Web Developer

Software Engineer

DevOps Engineer

ATS Score

Calculates an ATS compatibility score (0–100) based on:

resume length

skill presence

keywords

Resume Photo Extraction

Extracts profile photo directly from resume PDF.

Skill Gap Analysis

Shows missing skills between resume and job description.

Candidate Ranking

If multiple resumes are uploaded, the system ranks candidates automatically.

Recruiter Decision System

Recruiters can:

👍 Accept candidate

👎 Reject candidate

Automated Email Notification

When recruiter makes a decision:

Candidate receives professional email automatically

Candidate Report Generation

Generates a PDF report containing:

Candidate profile

Skills

Predicted role

Confidence score

Extracted links

Project Architecture 🏗
Resume Upload
      │
      ▼
Resume Parser (PyMuPDF)
      │
      ▼
Text Cleaning
      │
      ▼
TF-IDF Vectorization
      │
      ▼
ML Model Prediction
      │
      ▼
Skill Extraction + ATS Score
      │
      ▼
Recruiter Dashboard
      │
      ▼
Accept / Reject + Email Notification
Tech Stack 💻
Backend

Python

Flask

Machine Learning

Scikit-learn

TF-IDF Vectorizer

Resume Parsing

PyMuPDF

PyPDF2

File Processing

python-docx

Report Generation

ReportLab

Email Automation

SMTP (Gmail)

Project Structure 📂
resume_python/
│
├── templates/
│   └── index.html
│
├── data/
│   └── resume dataset
│
├── model.pkl
├── vectorizer.pkl
│
├── app.py
├── model_training.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env
Installation ⚙️
1 Clone the repository
git clone https://github.com/yourusername/ai-recruitment-assistant.git
2 Navigate into the project
cd ai-recruitment-assistant
3 Create virtual environment
python -m venv venv
4 Activate environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
5 Install dependencies
pip install -r requirements.txt
Environment Variables 🔐

Create a .env file in the root directory.

EMAIL_PASSWORD=your_gmail_app_password

This is used for sending recruiter decision emails.

Run the Application ▶️
python app.py

Open browser:

http://127.0.0.1:5000
Example Workflow 🧠

1 Upload Resume
2 System extracts candidate details
3 AI predicts job role
4 ATS score calculated
5 Recruiter reviews candidate
6 Recruiter clicks Accept / Reject
7 Candidate receives automated email