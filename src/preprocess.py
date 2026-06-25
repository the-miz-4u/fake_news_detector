import re
from indicnlp.transliterate.unicode_transliterate import ItransTransliterator

def clean_noise(text):
    """
    Noise removal step: Links, extra spaces, aur faltu characters hatata hai.
    """
    # URLs hatane ke liye
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # Extra spaces hatane ke liye
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def transliterate_hindi_to_roman(text):
    """
    Devanagari text ko Roman (ITRANS) format mein convert karta hai.
    """
    try:
        # 'hi' parameter ka matlab hai ki input Hindi (Devanagari) hai
        roman_text = ItransTransliterator.to_itrans(text, 'hi')
        return roman_text
    except Exception as e:
        print(f"Transliteration error: {e}")
        return text  # Agar koi word convert na ho paye, toh original text wapas bhej do

def preprocess_claim(text):
    """
    Pipeline Stage 1: Ye function user ke text ko poori tarah process karega.
    """
    # 1. Sabse pehle noise removal
    cleaned_text = clean_noise(text)
    
    # 2. Transliteration (Devanagari to Roman via IndicNLP)
    final_text = transliterate_hindi_to_roman(cleaned_text)
    
    return final_text