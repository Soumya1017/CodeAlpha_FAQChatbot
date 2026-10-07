# CodeAlpha_FAQChatbot

An FAQ chatbot for a fictional online store, **ShopEasy**, built for the CodeAlpha AI internship (Task 2).

## How it works
1. FAQs (questions and answers) are stored in `faqs.json`.
2. Text is cleaned with NLTK: lowercased, punctuation removed, and words reduced to their stems (e.g. "opening" becomes "open").
3. Questions are converted to numbers with TF-IDF.
4. Cosine similarity finds the FAQ closest to the user's question.
5. The best answer is returned. If the match score is too low, the bot says it didn't understand.

## Features
- 88 FAQs covering orders, shipping, payments, returns, cancellations, reviews, and accounts
- Terminal chatbot (`chatbot.py`)
- Streamlit chat window (`app.py`)

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python chatbot.py        # terminal version
streamlit run app.py     # chat window in the browser
```

## Limitations
- Matches on words, not meaning, so unusual phrasings may fail
- Cannot fix spelling mistakes
- Fix: add more phrasings to `faqs.json`

## Tech
Python, NLTK, scikit-learn, Streamlit