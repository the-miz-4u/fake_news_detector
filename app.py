from flask import Flask, render_template, request, jsonify
from src.prediction import predict_news
from google import genai
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


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
        # Step 1: Apne local PyTorch model se prediction lena
        result, confidence = predict_news(text) 
        
        # Step 2: Naye Google GenAI SDK aur Gemini 2.5 Flash ka use karna
        prompt = f"You are a fact-checking assistant. The following news claim is predicted to be {result}. Briefly explain in 2-3 sentences in Hinglish why this might be {result}. News: \"{text}\""
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        explanation = response.text
            
    except Exception as e:
        print("Backend Error:", str(e))
        explanation = f"AI Explanation currently unavailable. Error: {str(e)}"
    
    return jsonify({
        "prediction": result,
        "confidence": confidence,
        "explanation": explanation
    })

if __name__ == '__main__':
    app.run(debug=True)