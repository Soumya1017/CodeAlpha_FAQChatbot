# CodeAlpha_FAQChatbot

An FAQ chatbot for a fictional online store, **ShopEasy**, built for the CodeAlpha AI internship (Task 2).


## How it works
1. FAQs (questions and answers) are stored in `faqs.json`.
2. The user's text is cleaned: lowercased, punctuation removed, small spelling mistakes corrected, and words reduced to their stems with **NLTK** (e.g. "opening" becomes "open").
3. Common words are removed and the text is turned into numbers with **TF-IDF** (scikit-learn).
4. **Cosine similarity** finds the FAQ question closest to the user's question.
5. The matching answer is returned. If the best score is below 0.2, the bot says it did not understand.

## Features
- 102 FAQ entries covering orders, shipping, payments, returns, cancellations, reviews and accounts
- Spelling correction for small typos (e.g. "reiviews" becomes "reviews")
- Terminal chatbot (`chatbot.py`)
- Streamlit chat window with sample questions and a Clear chat button (`app.py`)

## Project structure
| File | Purpose |
|---|---|
| `faqs.json` | The FAQ questions and answers |
| `faq_engine.py` | Text cleaning, TF-IDF, cosine similarity (the bot's logic) |
| `chatbot.py` | Terminal interface |
| `app.py` | Streamlit web interface |
| `requirements.txt` | Libraries to install |

## Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

## Run
```bash
python chatbot.py        # terminal version
streamlit run app.py     # chat window in the browser
```

## Limitations
- It matches words, not meaning, so a question with no words in common with any FAQ will not be understood (e.g. "money back" vs "refund" needs both phrasings in `faqs.json`).
- Spelling correction only fixes small typos.
- To improve it, add more phrasings of a question to `faqs.json`, or use word embeddings in future.

## Tech
Python, NLTK, scikit-learn, Streamlit