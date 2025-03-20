from flask import Flask, request, render_template, jsonify
import joblib
import tensorflow as tf
import cv2
import pytesseract
import requests
import numpy as np
import re
import string

app = Flask(__name__)

# Load the model and vectorizer
model = joblib.load("sentiment_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


# Set Tesseract path (Update if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = re.sub("<.*?>", "", text)
    text = re.sub("\\d+", "", text)
    return text.strip()

# Function to predict sentiment
def predict_sentiment_from_text(text):
    text_cleaned = clean_text(text)
    text_vec = vectorizer.transform([text_cleaned])
    prediction = model.predict(text_vec)[0]
    return "Positive" if prediction == 1 else "Negative"

# Sentiment prediction for text input
@app.route("/predict-text", methods=["POST"])
def predict_text():
    data = request.get_json()
    sentiment = predict_sentiment_from_text(data["text"])
    return jsonify({"sentiment": sentiment})

# Sentiment prediction for uploaded image
@app.route("/predict-image", methods=["POST"])
def predict_image():
    if "file" not in request.files:
        return jsonify({"error": "No file provided."})
    
    file = request.files["file"]
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    if image is None:
        return jsonify({"error": "Invalid image file."})
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray).strip()

    print(f"Extracted text from image: {text}")  # Debugging output
    
    if text:
        sentiment = predict_sentiment_from_text(text)
        return jsonify({"sentiment": sentiment, "extracted_text": text})
    
    return jsonify({"error": "No readable text found in image."})

# Sentiment prediction for image URL
@app.route("/predict-url", methods=["POST"])
def predict_url():
    data = request.get_json()
    image_url = data.get("url", "").strip()
    
    if not image_url:
        return jsonify({"error": "No URL provided."})
    
    try:
        response = requests.get(image_url, stream=True, timeout=5)
        response.raise_for_status()  # Raise error for non-200 responses

        image = cv2.imdecode(np.asarray(bytearray(response.content), dtype=np.uint8), cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Invalid image format."})
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray).strip()

        print(f"Extracted text from URL image: {text}")  # Debugging output

        if text:
            sentiment = predict_sentiment_from_text(text)
            return jsonify({"sentiment": sentiment, "extracted_text": text})
        
        return jsonify({"error": "No readable text found in image."})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch image: {str(e)}"})

# Home route
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
