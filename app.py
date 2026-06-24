from flask import Flask, render_template, request, jsonify
# Nayi preprocessing script import kar rahe hain
from src.preprocess import preprocess_claim

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    raw_text = data.get('text', '')
    
    # Stage 1: Text Preprocessing
    processed_text = preprocess_claim(raw_text)
    
    response = {
        "status": "success",
        "original_claim": raw_text,
        "processed_claim": processed_text, # Ab hum clean text bhi bhej rahe hain
        "prediction": "Pending...", 
        "confidence": "N/A",
        "explanation": f"Pipeline ne aapke text ko clean kar diya hai: '{processed_text}'"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)