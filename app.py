from flask import Flask, render_template, request, jsonify
from src.prediction import predict_news
from google import genai
import os
import re
import requests
from bs4 import BeautifulSoup
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

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(10), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# API Client Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_text = data.get('text', '').strip()
    
    try:
        # FALLBACK: Start mein hi assign kar do taaki UnboundLocalError kabhi na aaye
        text_to_analyze = input_text
        display_text = input_text

        # URL Detection aur Web Scraping logic
        url_pattern = re.compile(r'^https?://\S+$', re.IGNORECASE)
        
        if url_pattern.match(input_text):
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(input_text, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            paragraphs = soup.find_all('p')
            scraped_text = " ".join([p.get_text() for p in paragraphs])
            
            if not scraped_text.strip():
                return jsonify({"error": "Website se koi text nahi nikal paya."}), 400
            
            # Wikipedia ke [1], [2] jaise references remove karna aur text clean karna
            clean_text = re.sub(r'\[\d+\]', '', scraped_text)
            text_to_analyze = clean_text[:500].strip() 
            display_text = f"[Scraped from URL] {text_to_analyze[:100]}..."

        # 1. Local PyTorch Model se Prediction lena
        # Ab yahan error nahi aayega kyunki variable humesha defined rahega
        result, confidence = predict_news(text_to_analyze) 
        
        # 2. Gemini 2.5 Flash se Hinglish Explanation lena
        prompt = f"You are a fact-checking assistant. The following news claim is predicted to be {result}. Briefly explain in 2-3 sentences in Hinglish why this might be {result}. News: \"{text_to_analyze}\""
        
        ai_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        explanation = ai_response.text
        
        # 3. Database me record save karna
        new_search = SearchHistory(text=display_text, prediction=result, confidence=confidence)
        db.session.add(new_search)
        db.session.commit()
            
    except Exception as e:
        print("Backend Error:", str(e))
        # Tumhara custom error message style
        return jsonify({"error": f"Kuch galat ho gaya: {str(e)}"}), 500
    
    return jsonify({
        "prediction": result,
        "confidence": confidence,
        "explanation": explanation
    })

@app.route('/history', methods=['GET'])
def get_history():
    records = SearchHistory.query.order_by(SearchHistory.timestamp.desc()).limit(5).all()
    history_data = []
    for r in records:
        history_data.append({
            "text": r.text,
            "prediction": r.prediction,
            "confidence": round(r.confidence, 2)
        })
    return jsonify(history_data)

# --- NAYA: Recent History Fetch Karne Ka Route ---
@app.route('/history', methods=['GET'])
def get_history():
    try:
        # Database se latest 5 searches nikalna (id ke descending order mein)
        recent_searches = SearchHistory.query.order_by(SearchHistory.id.desc()).limit(5).all()
        
        history_list = []
        for item in recent_searches:
            history_list.append({
                "id": item.id,
                "text": item.text[:80] + "..." if len(item.text) > 80 else item.text, # Zyada lamba text truncate karna
                "prediction": item.prediction,
                "confidence": item.confidence
            })
            
        return jsonify(history_list)
    except Exception as e:
        print("History Fetch Error:", str(e))
        return jsonify({"error": "History laane mein problem hui."}), 500

if __name__ == '__main__':
    app.run(debug=True)
