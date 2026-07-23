# 🚀 AI Fake News Detector

An end-to-end Full-Stack Machine Learning web application designed to detect, analyze, and explain fake news using Advanced NLP, PyTorch, and Google Gemini 2.5 Flash Generative AI. 

This project goes beyond simple classification by providing logical reasoning for its predictions, extracting text directly from live URLs, and visualizing app analytics in real-time.

---

## ✨ Key Features

* **🧠 Deep Learning + GenAI Validation:** Uses a local PyTorch NLP model for initial classification and Google Gemini 2.5 Flash for generating logical, easy-to-understand explanations in Hinglish.
* **🌐 Live URL Web Scraping:** Paste any news article link. The system automatically scrapes the main text using `BeautifulSoup` and verifies the claim.
* **🎤 Voice Input Integration:** Hands-free operation using the Web Speech API to dictate news claims directly in Hindi/Hinglish.
* **📊 Real-Time Analytics Dashboard:** A live, dynamic Donut Chart (powered by `Chart.js`) showing the ratio of Real vs. Fake news checked on the platform.
* **📲 WhatsApp Viral Sharing:** A dedicated button to format the AI's prediction, confidence score, and detailed reasoning, ready to be forwarded instantly on WhatsApp to curb misinformation.
* **🗄️ Database Integration & History:** Powered by SQLite and SQLAlchemy to maintain a session history of recent searches.
* **👍👎 ML Data Collection Pipeline:** Built-in user feedback mechanism to rate the AI's accuracy, storing data for future model retraining.
* **🌓 UI/UX:** Fully responsive, modern UI with Dark/Light mode toggle, dynamic typewriter effects, and an interactive "Architecture Modal".

---

## 💻 Tech Stack

**Frontend (Client-Side)**
* HTML5, CSS3, Vanilla JavaScript
* Chart.js (Data Visualization)
* Web Speech API (Voice Recognition)

**Backend (Server-Side)**
* Python 3
* Flask (Web Framework)
* SQLite & Flask-SQLAlchemy (Database)
* BeautifulSoup4 (Web Scraping & Data Extraction)

**Machine Learning & AI**
* PyTorch (Text Classification Model)
* Google Gemini API (Generative Reasoning)

---

## ⚙️ Installation & Setup Guide

Follow these steps to run the project on your local machine:

**1. Clone the Repository**
git clone https://github.com/the-miz-4u/Fake_News_Detector.git
cd Fake_News_Detector

**2. Create a Virtual Environment (Recommended)**
python -m venv venv
venv\Scripts\activate  # For Windows
# source venv/bin/activate  # For Mac/Linux

**3. Install Dependencies**
pip install flask flask-sqlalchemy requests beautifulsoup4 google-genai python-dotenv torch torchvision torchaudio

**4. Set Up Environment Variables**
Create a file named `.env` in the root directory and add your Google Gemini API key:
GEMINI_API_KEY=your_actual_api_key_here

**5. Run the Application**
python app.py

Open your web browser and go to: `http://127.0.0.1:5000/`

---

## 🏗️ Future Scope

* **Admin Dashboard:** To export collected user feedback (SQLite to CSV) for retraining the primary NLP model.
* **Multi-lingual Support:** Extending scraping and classification to regional Indian languages.
* **Browser Extension:** Checking news directly from WhatsApp Web or Facebook via a Chrome Extension.

---

## 👨‍💻 Developer Profile

**Manish Sharma**  
*B.Tech in Computer Science and Engineering (2023 - 2027)*  
*University of Engineering and Management (UEM), Jaipur*  

Passionate about Software Engineering, Machine Learning (NLP/LLMs), and building Full-Stack scalable systems.