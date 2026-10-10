from faq_engine import FAQBot

bot = FAQBot("faqs.json")

print("FAQ Chatbot ready! Type 'quit' to exit.")

while True:
    user_input = input("You: ")
    if user_input.lower().strip() in ["quit", "exit"]:
        print("Bot: Goodbye!")
        break
    print("Bot:", bot.answer(user_input))