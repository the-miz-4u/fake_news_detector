from flask import Flask, render_template, request, jsonify
from src.preprocess import preprocess_claim
from src.language_id import calculate_code_switching_density

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    raw_text = data.get('text', '')
    
    # Stage 1: Text Preprocessing (Noise removal & Transliteration)
    processed_text = preprocess_claim(raw_text)
    
    # Stage 2: Code-Switching Density (Token-level Language ID)
    # Original text par density nikalna zyada accurate hota hai
    density, tags = calculate_code_switching_density(raw_text)
    
    response = {
        "status": "success",
        "original_claim": raw_text,
        "processed_claim": processed_text,
        "cs_density": density,
        "token_tags": tags,
        "prediction": "Pending...", 
        "confidence": "N/A",
        "explanation": f"Pipeline Stage 2 Complete. Code-Switching Density is {density}."
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)