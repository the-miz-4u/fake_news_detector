from flask import Flask, render_template, request, jsonify
from src.prediction import predict_news

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')
    
    # Seedha prediction file se call lagayenge (jahan model already set hai)
    # Ab yeh function 2 cheezein dega: Result aur Confidence Score
    result, confidence = predict_news(text) 
    
    return jsonify({
        "prediction": result,
        "confidence": confidence
    })

if __name__ == '__main__':
    app.run(debug=True)