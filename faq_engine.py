import difflib
import json
import re

from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

THRESHOLD = 0.2
NO_MATCH = "Sorry, I didn't understand that. Try rephrasing your question."

stemmer = PorterStemmer()
# Keep "where": "Where is my order?" (tracking) must differ from "How can I order?"
STOP_WORDS = list(ENGLISH_STOP_WORDS - {"where"})


def tokenize(text):
    return re.findall(r"[a-z]+", text.lower())


class FAQBot:
    def __init__(self, path="faqs.json"):
        with open(path, "r", encoding="utf-8") as f:
            faqs = json.load(f)
        self.questions = [item["question"] for item in faqs]
        self.answers = [item["answer"] for item in faqs]
        # every word used in the FAQ questions, used to fix spelling mistakes
        self.vocab = sorted({w for q in self.questions for w in tokenize(q)})
        self.vectorizer = TfidfVectorizer(stop_words=STOP_WORDS)
        self.vectors = self.vectorizer.fit_transform(
            [self.preprocess(q) for q in self.questions]
        )

    def correct(self, word):
        if word in self.vocab or word in ENGLISH_STOP_WORDS:
            return word
        match = difflib.get_close_matches(word, self.vocab, n=1, cutoff=0.8)
        return match[0] if match else word

    def preprocess(self, text):
        words = [self.correct(w) for w in tokenize(text)]
        return " ".join(stemmer.stem(w) for w in words)

    def answer(self, user_input):
        user_vector = self.vectorizer.transform([self.preprocess(user_input)])
        scores = cosine_similarity(user_vector, self.vectors)[0]
        best = scores.argmax()
        if scores[best] > THRESHOLD:
            return self.answers[best]
        return NO_MATCH

    def best_question(self, user_input):
        user_vector = self.vectorizer.transform([self.preprocess(user_input)])
        scores = cosine_similarity(user_vector, self.vectors)[0]
        best = scores.argmax()
        return self.questions[best], float(scores[best])