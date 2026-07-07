from flask import Flask, render_template, request, jsonify
from src.prediction import predict_news
from google import genai
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# .env file load karna
load_dotenv()

app = Flask(__name__)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Table Setup
class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(10), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# App start hone par table automatically create kar dega (agar nahi hai toh)
with app.app_context():
    db.create_all()
# ------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')
    
    try:
        # Prediction lena
        result, confidence = predict_news(text) 
        
        # Gemini Explanation
        prompt = f"You are a fact-checking assistant. The following news claim is predicted to be {result}. Briefly explain in 2-3 sentences in Hinglish why this might be {result}. News: \"{text}\""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        explanation = response.text
        
        # --- NAYA: Database me record save karna ---
        new_search = SearchHistory(text=text, prediction=result, confidence=confidence)
        db.session.add(new_search)
        db.session.commit()
            
    except Exception as e:
        print("Backend Error:", str(e))
        explanation = f"AI Explanation currently unavailable. Error: {str(e)}"
    
    return jsonify({
        "prediction": result,
        "confidence": confidence,
        "explanation": explanation
    })

# --- NAYA: UI ko history bhejne wala route ---
@app.route('/history', methods=['GET'])
def get_history():
    # Last 5 searches nikalna database se (descending order)
    records = SearchHistory.query.order_by(SearchHistory.timestamp.desc()).limit(5).all()
    history_data = []
    for r in records:
        history_data.append({
            "text": r.text,
            "prediction": r.prediction,
            "confidence": round(r.confidence, 2)
        })
    return jsonify(history_data)

if __name__ == '__main__':
    app.run(debug=True)