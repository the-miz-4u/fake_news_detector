import re

def clean_noise(text):
    """
    Noise removal step: Links, extra spaces, aur faltu characters hatata hai.
    """
    # URLs hatane ke liye
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # Extra spaces hatane ke liye
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_claim(text):
    """
    Pipeline Stage 1: Ye function user ke text ko process karega.
    """
    # 1. Sabse pehle noise removal
    cleaned_text = clean_noise(text)
    
    # 2. Transliteration (Devanagari to Roman via IndicNLP)
    # Note: Isko hum aage setup karenge kyunki iske liye extra resource files lagti hain
    final_text = cleaned_text 
    
    return final_text