import re
import fitz  # PyMuPDF

# Extract text from uploaded PDF
def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        document = fitz.open(pdf_path)

        for page in document:
            text += page.get_text()

        document.close()

    except Exception as e:
        print("Error reading PDF:", e)

    return text


# Clean resume text
def clean_resume(text):

    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'RT|cc', ' ', text)
    text = re.sub(r'#\S+', ' ', text)
    text = re.sub(r'@\S+', ' ', text)
    text = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"""), ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.lower().strip()

# Basic technical skills list
SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Flask",
    "Django",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Power BI",
    "Tableau",
    "Excel",
    "Git",
    "GitHub",
    "AWS",
    "Docker",
    "MongoDB",
    "MySQL"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))

import re

EDUCATION_KEYWORDS = [
    "b.tech", "btech", "be", "b.e",
    "m.tech", "mtech", "mca",
    "bca", "bsc", "msc"
]

CERTIFICATION_KEYWORDS = [
    "certification",
    "certificate",
    "aws",
    "google",
    "microsoft",
    "oracle",
    "cisco",
    "coursera",
    "udemy"
]

PROJECT_KEYWORDS = [
    "project",
    "developed",
    "implemented",
    "created",
    "designed"
]

EXPERIENCE_KEYWORDS = [
    "intern",
    "internship",
    "experience",
    "worked",
    "developer",
    "engineer"
]


def calculate_resume_score(text, skills):

    score = 0
    suggestions = []

    text = text.lower()

    # ---------------- Skills ----------------

    skills_score = min(len(skills) * 2, 40)
    score += skills_score

    if skills_score < 20:
        suggestions.append("Add more technical skills.")

    # ---------------- Education ----------------

    if any(word in text for word in EDUCATION_KEYWORDS):
        score += 15
    else:
        suggestions.append("Mention your education clearly.")

    # ---------------- Projects ----------------

    if any(word in text for word in PROJECT_KEYWORDS):
        score += 10
    else:
        suggestions.append("Include academic or personal projects.")

    # ---------------- Experience ----------------

    if any(word in text for word in EXPERIENCE_KEYWORDS):
        score += 20
    else:
        suggestions.append("Mention internship or work experience.")

    # ---------------- Certifications ----------------

    if any(word in text for word in CERTIFICATION_KEYWORDS):
        score += 10
    else:
        suggestions.append("Add certifications if available.")

    # ---------------- Contact ----------------

    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

    phone = re.search(r"\b\d{10}\b", text)

    linkedin = "linkedin" in text

    if email:
        score += 2

    if phone:
        score += 2

    if linkedin:
        score += 1
    else:
        suggestions.append("Add your LinkedIn profile.")

    score = min(score, 100)

    return score, suggestions