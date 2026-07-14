import nltk

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib

from utils import (
    extract_text_from_pdf,
    clean_resume,
    extract_skills,
    calculate_resume_score
)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -----------------------------
# Load Model & TF-IDF
# -----------------------------
model = joblib.load("model.pkl")
tfidf = joblib.load("tfidf.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Resume Screening API is Running"
    })


# -----------------------------
# Predict Route
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    if "resume" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Please choose a PDF file"
        }), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    # Extract text
    resume_text = extract_text_from_pdf(filepath)

    # Clean text
    cleaned_text = clean_resume(resume_text)

    # TF-IDF Transformation
    vector = tfidf.transform([cleaned_text])

    # Prediction
    prediction = model.predict(vector)[0]
    prediction = label_encoder.inverse_transform([prediction])[0]
    skills = extract_skills(resume_text)
    resume_score, suggestions = calculate_resume_score(
    resume_text,
    skills
)

    # Delete uploaded file
    os.remove(filepath)

    return jsonify({
    "success": True,
    "prediction": prediction,
    "skills": skills,
    "resume_score": resume_score,
    "suggestions": suggestions
})


if __name__ == "__main__":
    app.run(debug=True)