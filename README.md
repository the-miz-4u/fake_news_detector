# 📰 AI Fake News Detector (Hindi & Hinglish)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-ee4c2c)
![Flask](https://img.shields.io/badge/Flask-Backend-000000)
![Status](https://img.shields.io/badge/Status-Completed-success)

A highly accurate, dual-embedding machine learning project designed to detect fake news claims in pure Hindi and code-mixed Hinglish text. It utilizes a state-of-the-art NLP pipeline with a modern, responsive web interface.

---

## 🚀 Key Features

* **Bilingual NLP Support:** Capable of understanding and processing both Hindi and Hinglish (code-mixed) textual data.
* **Dual-Embedding Architecture:** Combines the power of **XLM-RoBERTa** (Cross-lingual understanding) and **Google's MuRIL** (specifically pre-trained on Indian languages) for deep contextual analysis.
* **Modern Web Interface:** A clean, card-based responsive UI with smooth animations and dynamic result rendering.
* **Real-time Processing:** Asynchronous backend calls using JavaScript `fetch` API with interactive loading states (Spinners) for better User Experience (UX).

---

## 🛠️ Tech Stack

### Machine Learning & NLP
* **Frameworks:** PyTorch, HuggingFace Transformers
* **Models:** `xlm-roberta-base`, `google/muril-base-cased`
* **Data Processing:** Pandas, Scikit-learn, SentencePiece

### Backend & API
* **Framework:** Flask (Python)
* **API Architecture:** RESTful structure accepting JSON payloads.

### Frontend
* **Technologies:** HTML5, CSS3, Vanilla JavaScript
* **Design:** Custom CSS with Google Fonts (Poppins), fully responsive layout.

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally on your machine:

**1. Clone the repository**
```bash
git clone [https://github.com/your-username/fake_news_detector.git](https://github.com/your-username/fake_news_detector.git)
cd fake_news_detector
```

**2. Install dependencies**
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

**3. Add the Pre-trained Model**
* Due to GitHub's file size limits, the trained model (`dual_embedding_model.pth`) is not included in the repository.
* Place your trained `.pth` file inside the `models/` directory.

**4. Run the Flask Server**
```bash
python app.py
```

**5. Access the Web App**
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 📂 Project Structure

```text
fake_news_detector/
│
├── models/
│   └── dual_embedding_model.pth    # Trained PyTorch model (Local only)
│
├── templates/
│   └── index.html                  # Modern Frontend UI
│
├── app.py                          # Flask Backend Application
├── requirements.txt                # Project Dependencies
├── .gitignore                      # Git ignore rules (excluding .pth)
└── README.md                       # Project Documentation
```

---

## 👨‍💻 Author

**Manish Sharma**  
