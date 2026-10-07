import json
import re
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

stemmer = PorterStemmer()


def preprocess(text):
    tokens = re.findall(r"[a-z]+", text.lower())
    return " ".join(stemmer.stem(t) for t in tokens)


with open("faqs.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

questions = [item["question"] for item in faqs]
answers = [item["answer"] for item in faqs]

processed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer(stop_words="english")
faq_vectors = vectorizer.fit_transform(processed_questions)

print("FAQ Chatbot ready! Type 'quit' to exit.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        print("Bot: Goodbye!")
        break

    user_vector = vectorizer.transform([preprocess(user_input)])
    scores = cosine_similarity(user_vector, faq_vectors)[0]
    best = scores.argmax()

    if scores[best] > 0.2:
        print("Bot:", answers[best])
    else:
        print("Bot: Sorry, I didn't understand that.")