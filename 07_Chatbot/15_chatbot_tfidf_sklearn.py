"""Optional ML chatbot using TF-IDF + logistic regression.
Install: python -m pip install scikit-learn
This is a small educational intent classifier, not a generative AI assistant.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

examples = [
    "hello", "hi there", "good morning", "hey", "goodbye", "bye", "see you",
    "thank you", "thanks a lot", "help me", "what can you do", "show features",
    "when are you open", "what are your hours", "show the timetable", "class schedule"
]
labels = [
    "greeting", "greeting", "greeting", "greeting", "goodbye", "goodbye", "goodbye",
    "thanks", "thanks", "help", "help", "help", "hours", "hours", "schedule", "schedule"
]
responses = {
    "greeting": "Hello! How can I help?",
    "goodbye": "Goodbye!",
    "thanks": "You're welcome!",
    "help": "I can answer basic questions. Add more training examples to expand me.",
    "hours": "Please check the official opening-hours notice.",
    "schedule": "Please check the official timetable.",
    "unknown": "I am not sure I understood. Could you rephrase?"
}
model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000))
model.fit(examples, labels)

if __name__ == "__main__":
    print("Bot: Hello! Type exit to stop.")
    while True:
        text = input("You: ").strip()
        if text.lower() in {"exit", "quit", "bye"}:
            print("Bot:", responses["goodbye"])
            break
        if not text:
            print("Bot: Please type a message.")
            continue
        probabilities = model.predict_proba([text])[0]
        idx = probabilities.argmax()
        intent = model.classes_[idx] if probabilities[idx] >= 0.40 else "unknown"
        print("Bot:", responses[intent])
