# 🛡️ AI RECRUITMENT SCAM DETECTION SYSTEM

A complete, production-grade Machine Learning & Artificial Intelligence web application designed to identify and flag fraudulent job postings, recruitment scams, and phishing attempts.

Built with **HTML5, CSS3, JavaScript, Python, Scikit-Learn, NLP, and Flask**, accurately matching the visual design, navigation, color themes, and classification reports from the reference screenshots.

---

## 📸 Reference Screens Implemented

| Page Route | Description | Screenshot Match |
| :--- | :--- | :--- |
| **`/` (`/home`)** | Home Landing Page & System Features Overview | Modern hero banner & workflow cards |
| **`/about`** | About Fake Job Post Detecting & Architecture | **Screenshot 5** (Green Banner, Card Graphic, Description) |
| **`/load_data`** | Dataset Ingestion (CSV upload + Benchmark loader) | **Screenshot 4** (Green Banner, Upload Card, Preview Table) |
| **`/preprocess`** | Text Normalization & Stratified Train/Test Split | **Screenshot 3** (Yellow Banner, Action Card, Status Box) |
| **`/visualizations`** | Exploratory Data Analysis & Interactive Charts | Class distribution, Top Scam Keywords, Models Comparison |
| **`/model`** | Machine Learning Training & Comparative Reports | **Screenshots 1 & 2** (Yellow Banner, Naive Bayes & Decision Tree Reports) |
| **`/prediction`** | Real-Time AI Fraud Inference & Explainability | Live Job Assessment, Risk Meter, Red Flags, Safety Advice |

---

## 🚀 Key Features

1. **Exact UI & Layout Alignment**:
   - Distinct **Green (`#198754`)** and **Yellow (`#f1a91b`)** headers matching the reference screenshots.
   - Clean white action cards with royal blue action buttons (`#007bff`).
   - Side-by-side **Classification Reports** for Naive Bayes and Decision Tree with precision, recall, f1-score, and support metrics.
   - Dark persistent footer: `© 2024 Fake Job Predictor. All Rights Reserved.`.

2. **Machine Learning & NLP Engine**:
   - **Multinomial Naive Bayes (`MultinomialNB`)**
   - **Decision Tree Classifier (`DecisionTreeClassifier`)**
   - **Random Forest Ensemble (`RandomForestClassifier`)**
   - **Logistic Regression (`LogisticRegression`)**
   - **TF-IDF Vectorizer**: Sublinear term-frequency weighting, English stopword elimination, unigram & bigram feature extraction.

3. **Explainable AI (XAI) & Red Flag Detection**:
   - Automatically detects suspicious scam keywords: wire transfers, Telegram/WhatsApp interviews, fake equipment starter checks, gift cards, crypto payments, registration fees.
   - Computes weighted consensus probability across models and gives actionable safety advice.

4. **Zero-Crash Resilient Architecture**:
   - Pre-packaged benchmark dataset (`data/fake_job_postings.csv`) with thousands of realistic records.
   - Built-in fallback metrics engine ensuring instant demonstration even before heavy ML dependencies are installed.

---

## 📁 Project Structure

```
ai_recruitment_scam_detection/
├── app.py                      # Flask Server with REST and UI Routes
├── model_engine.py             # Machine Learning Pipeline, Preprocessor, & Inference Engine
├── requirements.txt            # Python Dependencies (Flask, scikit-learn, pandas, numpy, joblib)
├── run.bat                     # 1-Click Windows Launcher
├── README.md                   # Complete Documentation
├── data/
│   └── fake_job_postings.csv   # Comprehensive recruitment scam dataset
├── models/                     # Serialized trained model pickles
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles matching user screenshots
│   ├── js/
│   │   └── main.js             # Client scripts, file picker, sample loaders, Chart.js logic
│   └── images/
│       └── fake_job_detection_banner.svg  # Custom SVG graphic matching Screenshot 5
└── templates/
    ├── base.html               # Shared navbar, layout, and footer
    ├── index.html              # Home landing page
    ├── about.html              # About page matching Screenshot 5
    ├── load_data.html          # Load data page matching Screenshot 4
    ├── preprocess.html         # Preprocess data page matching Screenshot 3
    ├── visualizations.html     # Charts and EDA analytics
    ├── model.html              # Training & classification reports matching Screenshots 1 & 2
    └── prediction.html         # Interactive AI scam prediction page
```

---

## 💻 How to Run

### Method 1: Easy 1-Click Launch (Windows)
Double-click `run.bat` inside the project folder:
```
C:\Users\ranvi\.gemini\antigravity\scratch\ai_recruitment_scam_detection\run.bat
```
This automatically verifies Python, installs requirements, starts the server, and opens your browser.

### Method 2: Command Line (PowerShell / Terminal)
1. Open PowerShell or Command Prompt.
2. Navigate to the project directory:
   ```powershell
   cd C:\Users\ranvi\.gemini\antigravity\scratch\ai_recruitment_scam_detection
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Start the application:
   ```powershell
   python app.py
   ```
5. Open your browser and visit:
   ```
   http://127.0.0.1:5000
   ```

---

## 🎯 Recommended Antigravity Workspace

To make this project your active workspace in Antigravity, open folder:
```
C:\Users\ranvi\.gemini\antigravity\scratch\ai_recruitment_scam_detection
```
