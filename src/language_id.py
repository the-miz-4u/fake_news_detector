import re

def get_token_language(word):
    """
    Token-level language identification.
    (Note: Asli IndicLID model yahan integrate hoga. Abhi pipeline structure 
    ready karne ke liye hum regex-based fallback use kar rahe hain.)
    """
    # Agar word mein Devanagari (Hindi) characters hain
    if re.search(r'[\u0900-\u097F]', word):
        return 'HI'
    # Agar word purely English alphabets hai
    elif re.match(r'^[a-zA-Z]+$', word):
        return 'EN'
    # Numbers, symbols, ya mixed alphanumeric
    else:
        return 'MIX'

def calculate_code_switching_density(text):
    """
    Text ko tokens mein tod kar language tag karta hai aur density nikalta hai.
    """
    tokens = text.split()
    if not tokens:
        return 0.0, []
    
    tags = []
    mix_or_hi_count = 0
    
    for token in tokens:
        lang = get_token_language(token)
        tags.append((token, lang))
        
        # Agar word Hindi ya Mixed hai, toh counter badhao
        if lang in ['HI', 'MIX']:
            mix_or_hi_count += 1
            
    # Density formula: (Hindi + Mixed tokens) / Total tokens
    density = round(mix_or_hi_count / len(tokens), 2)
    
    return density, tags