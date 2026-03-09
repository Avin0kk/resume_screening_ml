import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, send_file
import pickle
import re
from PyPDF2 import PdfReader
from docx import Document
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

SKILLS_DB = [
"python","java","c++","machine learning","deep learning",
"data analysis","sql","mysql","mongodb",
"html","css","javascript","react","node","flask",
"django","aws","docker","kubernetes",
"tensorflow","pandas","numpy","scikit-learn"
]

def clean_text(text):
    text=text.lower()
    text=re.sub(r'[^a-zA-Z ]','',text)
    text=re.sub(r'\s+',' ',text)
    return text

def extract_skills(text):
    return [skill.title() for skill in SKILLS_DB if skill in text]

def extract_text_from_pdf(file):
    reader=PdfReader(file)
    text=""
    for page in reader.pages:
        page_text=page.extract_text()
        if page_text:
            text+=page_text
    return text

def extract_text_from_docx(file):
    doc=Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def extract_links_from_pdf(file):

    links={
        "email":None,
        "linkedin":None,
        "github":None,
        "leetcode":None
    }

    pdf=fitz.open(stream=file.read(),filetype="pdf")

    for page in pdf:
        for link in page.get_links():

            uri=link.get("uri")

            if uri:
                if "mailto:" in uri:
                    links["email"]=uri.replace("mailto:","")

                elif "linkedin.com" in uri:
                    links["linkedin"]=uri

                elif "github.com" in uri:
                    links["github"]=uri

                elif "leetcode.com" in uri:
                    links["leetcode"]=uri

    return links

def extract_photo_from_pdf(file):

    pdf=fitz.open(stream=file.read(),filetype="pdf")

    for page in pdf:

        images=page.get_images()

        if images:

            xref=images[0][0]
            base_image=pdf.extract_image(xref)
            image_bytes=base_image["image"]

            with open("candidate_photo.png","wb") as f:
                f.write(image_bytes)

            return "candidate_photo.png"

    return None

def extract_experience(text):

    match=re.search(
        r'EXPERIENCE(.*?)EDUCATION',
        text,
        re.DOTALL|re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return None

def extract_basic_details(text,skills,links):

    phone_match=re.search(r'\+?\d[\d\s\-]{8,15}',text)
    phone=phone_match.group(0) if phone_match else None

    major_skill=skills[0] if skills else None

    name=text.split("\n")[0][:40]

    experience=extract_experience(text)

    return {
        "name":name,
        "email":links.get("email"),
        "phone":phone,
        "linkedin":links.get("linkedin"),
        "github":links.get("github"),
        "leetcode":links.get("leetcode"),
        "experience":experience,
        "major_skill":major_skill
    }

def calculate_ats_score(text):

    score=0
    word_count=len(text.split())

    if word_count>300:
        score+=30

    skills_found=extract_skills(text)
    score+=min(len(skills_found)*5,40)

    if "project" in text:
        score+=10
    if "experience" in text:
        score+=10

    return min(score,100)

def send_decision_email(email,name,decision):

    sender="goelavin543@gmail.com"
    password=os.getenv("EMAIL_PASSWORD")

    if not password:
        print("EMAIL PASSWORD NOT FOUND IN ENV")
        return

    if decision=="accept":

        subject="Application Status Update"

        body=f"""
Dear {name},

Congratulations!

After reviewing your resume, we are pleased to inform you that you have been shortlisted.

Our team will contact you soon regarding the next steps.

Best regards
Recruitment Team
"""

    else:

        subject="Application Status Update"

        body=f"""
Dear {name},

Thank you for applying.

After careful consideration, we regret to inform you that we will not proceed further with your application.

We wish you success in your future endeavors.

Best regards
Recruitment Team
"""

    msg=MIMEText(body)
    msg["Subject"]=subject
    msg["From"]=sender
    msg["To"]=email

    try:
        server=smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login(sender,password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print("Email sending failed:",e)

def generate_report(details,prediction,confidence,photo):

    filename="candidate_report.pdf"
    c=canvas.Canvas(filename,pagesize=letter)

    y=750

    c.drawString(100,y,"AI Recruitment Candidate Report")
    y-=40

    if photo:
        c.drawImage(photo,400,650,width=120,height=120)

    for key,value in details.items():

        if value:
            c.drawString(100,y,f"{key.capitalize()}: {value}")
            y-=25

    c.drawString(100,y,f"Predicted Role: {prediction}")
    y-=25

    c.drawString(100,y,f"Confidence: {confidence}%")

    c.save()

    return filename

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():

    resume_text=""
    photo=None
    links={}

    file = request.files.get('resume_file')

    if file and file.filename and file.filename.endswith(".pdf"):

        resume_text=extract_text_from_pdf(file)

        file.seek(0)
        links=extract_links_from_pdf(file)

        file.seek(0)
        photo=extract_photo_from_pdf(file)

    cleaned=clean_text(resume_text)

    skills=extract_skills(cleaned)

    details=extract_basic_details(resume_text,skills,links)

    transformed=vectorizer.transform([cleaned])
    probs=model.predict_proba(transformed)[0]

    top_indices=np.argsort(probs)[-3:][::-1]

    top_roles=[(model.classes_[i],round(probs[i]*100,2)) for i in top_indices]

    prediction=top_roles[0][0]
    confidence=top_roles[0][1]

    ats_score=calculate_ats_score(cleaned)

    suggestions=[
    "Add quantified achievements",
    "Mention measurable impact",
    "Include project links"
    ]

    generate_report(details,prediction,confidence,photo)

    return render_template(
    "index.html",
    prediction=prediction,
    confidence=confidence,
    skills=skills,
    top_roles=top_roles,
    ats_score=ats_score,
    suggestions=suggestions,
    details=details,
    photo=photo
    )

@app.route('/decision',methods=['POST'])
def decision():

    email=request.form.get("email")
    name=request.form.get("name")
    decision=request.form.get("decision")

    if email:
        send_decision_email(email,name,decision)
        message="Decision recorded and email sent ✔"

    else:
        message="Decision recorded but no email found in resume"

    return render_template("index.html",decision_message=message)

@app.route('/download_report')
def download_report():
    return send_file("candidate_report.pdf",as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)