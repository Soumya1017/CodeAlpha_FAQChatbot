import json
import re
import streamlit as st
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

stemmer = PorterStemmer()


def preprocess(text):
    tokens = re.findall(r"[a-z]+", text.lower())
    return " ".join(stemmer.stem(t) for t in tokens)


@st.cache_resource
def load_bot():
    with open("faqs.json", "r", encoding="utf-8") as f:
        faqs = json.load(f)
    questions = [item["question"] for item in faqs]
    answers = [item["answer"] for item in faqs]
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([preprocess(q) for q in questions])
    return vectorizer, vectors, answers


def get_answer(user_input):
    vectorizer, vectors, answers = load_bot()
    user_vector = vectorizer.transform([preprocess(user_input)])
    scores = cosine_similarity(user_vector, vectors)[0]
    best = scores.argmax()
    if scores[best] > 0.2:
        return answers[best]
    return "Sorry, I didn't understand that. Try rephrasing your question."


st.title("🛒 ShopEasy FAQ Chatbot")
st.caption("Ask me about orders, shipping, returns, payments, or your account.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    reply = get_answer(user_input)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)