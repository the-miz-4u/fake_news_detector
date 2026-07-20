import random

def predict_news(text):
    """
    Yeh ek dummy function hai jab tak tumhara asli PyTorch model 
    connect nahi ho jata. Yeh text ke basis par random Real/Fake dega.
    """
    # Thoda random logic (taaki UI test kar sako)
    confidence = round(random.uniform(75.0, 99.0), 2)
    
    if len(text) % 2 == 0 or "sach" in text.lower() or "real" in text.lower():
        return "Real", confidence
    else:
        return "Fake", confidence
        