import streamlit as st

from faq_engine import FAQBot


@st.cache_resource
def load_bot():
    return FAQBot("faqs.json")


bot = load_bot()

st.set_page_config(page_title="ShopEasy FAQ Chatbot", page_icon="🛒")
st.title("🛒 ShopEasy FAQ Chatbot")
st.caption("Ask me about orders, shipping, returns, cancellations, reviews, or your account.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Try asking")
    samples = [
        "How do I cancel my order?",
        "Where is my order?",
        "Can I get my money back?",
        "How do I write a review?",
        "Do you accept UPI?",
    ]
    for s in samples:
        if st.button(s, use_container_width=True):
            st.session_state.pending = s
    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write("Hi! I'm the ShopEasy assistant. Ask me a question or pick one from the sidebar.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

typed = st.chat_input("Type your question here...")
user_input = st.session_state.pop("pending", None) or typed

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    reply = bot.answer(user_input)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)