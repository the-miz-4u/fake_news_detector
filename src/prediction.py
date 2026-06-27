import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

# 1. Wahi same architecture jo Colab mein banaya tha
class DualEmbeddingFakeNewsModel(nn.Module):
    def __init__(self, num_labels=2):
        super(DualEmbeddingFakeNewsModel, self).__init__()
        self.xlm = AutoModel.from_pretrained("xlm-roberta-base")
        self.muril = AutoModel.from_pretrained("google/muril-base-cased")
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(768 * 2, num_labels)
        
    def forward(self, xlm_input_ids, xlm_attention_mask, muril_input_ids, muril_attention_mask):
        xlm_outputs = self.xlm(input_ids=xlm_input_ids, attention_mask=xlm_attention_mask)
        xlm_pooled = xlm_outputs.last_hidden_state[:, 0, :] 
        muril_outputs = self.muril(input_ids=muril_input_ids, attention_mask=muril_attention_mask)
        muril_pooled = muril_outputs.last_hidden_state[:, 0, :]
        combined = torch.cat((xlm_pooled, muril_pooled), dim=1)
        dropped = self.dropout(combined)
        return self.classifier(dropped)

# 2. Tokenizers aur Model Load Karna
print("Loading AI Model in Backend... (Isme thoda time lag sakta hai)")
xlm_tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
muril_tokenizer = AutoTokenizer.from_pretrained("google/muril-base-cased")

# Local laptop par inference ke liye CPU use karenge
device = torch.device("cpu")
model = DualEmbeddingFakeNewsModel()

# map_location='cpu' zaroori hai kyunki train GPU par hua tha
model.load_state_dict(torch.load('models/dual_embedding_model.pth', map_location=device))
model.eval() # Model ko testing mode mein set karna

def predict_news(text):
    """
    Naye text ko model mein bhej kar Real/Fake ka result nikalta hai.
    """
    # Text ko tokens mein todna
    xlm_enc = xlm_tokenizer(text, max_length=128, padding='max_length', truncation=True, return_tensors="pt")
    muril_enc = muril_tokenizer(text, max_length=128, padding='max_length', truncation=True, return_tensors="pt")
    
    with torch.no_grad(): # Inference ke time gradients calculate karne ki zarurat nahi
        outputs = model(
            xlm_enc['input_ids'], xlm_enc['attention_mask'],
            muril_enc['input_ids'], muril_enc['attention_mask']
        )
        
        # Softmax se probability nikalna
        probs = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_class = torch.max(probs, dim=1)
        
    # Colab wale dummy data ke hisab se: 0 = Real, 1 = Fake (Apne asli dataset ke hisab se ise adjust kar lena)
    label = "Fake" if predicted_class.item() == 1 else "Real"
    conf_score = round(confidence.item() * 100, 2)
    
    return label, conf_score