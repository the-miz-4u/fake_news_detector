import os
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from google import genai
from dotenv import load_dotenv

# --- Tumhare PyTorch Model ka Import ---
# DHYAN RAHE: Agar tumhara import function kisi aur naam se hai, toh usko update kar lena.
# Image ke hisaab se tumhari prediction.py file hai, toh hum wahi assume kar rahe hain.
from prediction import predict_news 

# --- App Configuration ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Gemini API Setup ---
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# --- Database Models ---
class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

class FeedbackData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    feedback_type = db.Column(db.String(10), nullable=False) # 'up' ya 'down'

# --- Routes ---
@app.route('/')
def index():
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
        return jsonify({"error": f"Kuch galat ho gaya: {str(e)}"}), 500
    
    return jsonify({
        "prediction": result,
        "confidence": confidence,
        "explanation": explanation
    })

@app.route('/history', methods=['GET'])
def get_history():
    try:
        # Database se latest 5 searches nikalna (id ke descending order mein)
        recent_searches = SearchHistory.query.order_by(SearchHistory.id.desc()).limit(5).all()
        
        history_list = []
        for item in recent_searches:
            history_list.append({
                "id": item.id,
                "text": item.text[:80] + "..." if len(item.text) > 80 else item.text,
                "prediction": item.prediction,
                "confidence": item.confidence
            })
            
        return jsonify(history_list)
    except Exception as e:
        print("History Fetch Error:", str(e))
        return jsonify({"error": "History laane mein problem hui."}), 500

@app.route('/feedback', methods=['POST'])
def save_feedback():
    data = request.get_json()
    try:
        new_feedback = FeedbackData(
            text=data.get('text', ''),
            prediction=data.get('prediction', ''),
            feedback_type=data.get('feedback', '')
        )
        db.session.add(new_feedback)
        db.session.commit()
        return jsonify({"status": "success", "message": "Feedback saved successfully!"})
    except Exception as e:
        print("Feedback Error:", str(e))
        return jsonify({"error": "Feedback save nahi hua."}), 500
    
# --- NAYA: Live Analytics Data Ka Route ---
@app.route('/analytics', methods=['GET'])
def get_analytics():
    try:
        real_count = SearchHistory.query.filter_by(prediction='Real').count()
        fake_count = SearchHistory.query.filter_by(prediction='Fake').count()
        return jsonify({"real": real_count, "fake": fake_count})
    except Exception as e:
        print("Analytics Error:", str(e))
        return jsonify({"error": "Data fetch nahi hua"}), 500

if __name__ == '__main__':
    # Yeh app_context wala code ensure karega ki nayi FeedbackData table Database me ban jaye
    with app.app_context():
        db.create_all()  
    app.run(debug=True)