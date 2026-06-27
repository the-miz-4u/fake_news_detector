from flask import Flask, render_template, request, jsonify
from src.preprocess import preprocess_claim
from src.language_id import calculate_code_switching_density
from src.prediction import predict_news

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
    
    # Stage 2: Code-Switching Density
    density, tags = calculate_code_switching_density(raw_text)
    
    # Stage 3: AI Model Prediction (Dual-Embedding)
    # Model ko cleaned text bhejte hain
    prediction_label, confidence = predict_news(processed_text)
    
    response = {
        "status": "success",
        "original_claim": raw_text,
        "processed_claim": processed_text,
        "cs_density": density,
        "token_tags": tags,
        "prediction": prediction_label, 
        "confidence": f"{confidence}%",
        "explanation": f"AI model is {confidence}% confident that this news is {prediction_label}."
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)