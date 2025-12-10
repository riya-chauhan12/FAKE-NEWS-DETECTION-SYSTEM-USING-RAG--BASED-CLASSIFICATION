📰  Fake News Detection System (ML + NLP + RAG-Based Verification)

A powerful end-to-end Fake News Detection System combining:

Machine Learning (TF-IDF + SVM)

NLP-based linguistic analysis

RAG-style semantic verification using Sentence Transformers

Multi-source evidence retrieval via GNews, NewsAPI, Bing

Article parsing with Newspaper3k + BeautifulSoup

Hybrid scoring algorithm for final truth classification

This project analyzes a claim, retrieves real news articles, extracts textual evidence, evaluates semantic similarity, and produces a final TRUE / FALSE / UNVERIFIABLE verdict.

🚀 Key Features
🔹 1. Machine Learning Style-Based Classifier

TF-IDF vectorization

Linear SVC classifier

Detects sensational language, all-caps words, emotional tone, clickbait patterns

🔹 2. Multi-Source News Evidence Search

Searches GNews API

Searches NewsAPI

Optional Bing News Search

Deduplicates articles

Assigns source reliability scores

🔹 3. Article Parsing & Preprocessing

Uses newspaper3k

Falls back to BeautifulSoup4

Filters out scripts, ads, navigation elements

🔹 4. RAG-Style Semantic Verification

Embedding model: all-MiniLM-L6-v2

Computes semantic similarity

Identifies supporting or refuting evidence

🔹 5. Hybrid Scoring Engine

Combines:

ML style score

Evidence support score

Source reliability

Semantic consistency

Produces:

TRUE

LIKELY TRUE

FALSE

LIKELY FALSE

UNVERIFIABLE

🔹 6. Evidence Presentation Layer

Outputs:

Summary

Supporting & refuting sources

Confidence scores

Key facts extracted from the articles

Linguistic analysis

🧰 Tech Stack

Languages: Python
ML: Scikit-Learn (TF-IDF, LinearSVC)
Embeddings: Sentence Transformers (MiniLM)
Search APIs: GNews, NewsAPI, Bing
Scraping: Newspaper3k, BeautifulSoup
Environment: VS Code, Git, GitHub

📁 Dataset

This project uses the publicly available Fake and Real News Dataset:

📌 Dataset Link (Kaggle)
https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset

Download the following files from Kaggle:

Fake.csv

True.csv

After downloading, place them in:

project-folder/
   data/
      Fake.csv
      True.csv


⚠️ These files are NOT included in this repository because they are large (50MB+) and exceed GitHub’s recommended file size limit.
They are automatically ignored using .gitignore.

📂 Project Structure
├── src/
│   ├── classifier.py         # ML-based fake news classifier
│   ├── searcher.py           # Multi-source evidence search
│   ├── parser.py             # Parses articles using Newspaper3k / BS4
│   ├── verifier.py           # RAG-style semantic verification
│   ├── scorer.py             # Hybrid scoring algorithm
│   ├── presenter.py          # Human-readable output formatting
│   └── main.py               # CLI entry point
│
├── models/
│   └── fake_news_model.pkl   # Trained model (gitignored)
│
├── data/
│   └── Fake.csv / True.csv   # (ignored)
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/riya-chauhan12/FAKE-NEWS-DETECTION-SYSTEM-USING-RAG--BASED-CLASSIFICATION.git
cd FAKE-NEWS-DETECTION-SYSTEM-USING-RAG--BASED-CLASSIFICATION

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Add Your API Keys

Open src/main.py and add:

api_keys = {
    "gnews": "YOUR_GNEWS_KEY",
    "newsapi": "YOUR_NEWSAPI_KEY",
    "bing": "YOUR_BING_KEY"  # optional
}


Free keys:

https://gnews.io

https://newsapi.org

▶️ How to Run
python src/main.py


You will be prompted:

Enter a claim to verify:


Example input:

"NASA confirms alien life discovered on Mars"


Example output:

⚖️ Verdict: FALSE
📊 Confidence: 88.2%
💭 Reasoning: Refuted by 3 reliable sources
📝 Summary: Evidence contradicts the claim across multiple outlets.
🔍 Linguistic Analysis: Detects sensational and emotional wording.

🔮 Future Improvements

Add LLM (GPT-4 or Gemini) cross-verification

Deploy as Streamlit web app

Build a REST API server

Add topic classification (politics, health, finance, etc.)

Use FAISS vector database for better retrieval

🤝 Contributing  
Contributions are welcome!  
For major changes, please discuss them with me first.


📜 License
This project is released under the MIT License, allowing free use and modification with attribution.
