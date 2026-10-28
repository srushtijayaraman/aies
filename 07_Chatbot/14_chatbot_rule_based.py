"""Standalone rule-based chatbot; no external libraries required."""
import re

def reply(message):
    text = message.lower().strip()
    words = set(re.findall(r"[a-z']+", text))
    if not text:
        return "Please type a message."
    if words & {"bye", "goodbye", "quit", "exit"}:
        return "Goodbye!"
    if words & {"hi", "hello", "hey", "morning"}:
        return "Hello! How can I help you?"
    if "thank" in words or "thanks" in words:
        return "You're welcome!"
    if words & {"help", "features", "do"}:
        return "I can answer basic greetings, help requests, and course questions."
    if "assignment" in words or "lab" in words:
        return "Tell me which AI lab assignment you are working on."
    if "time" in words or "hours" in words:
        return "Please check the official timetable or opening-hours notice."
    return "I did not understand that. Try asking in a different way."

if __name__ == "__main__":
    print("Bot: Hi! Type 'exit' to quit.")
    while True:
        message = input("You: ")
        answer = reply(message)
        print("Bot:", answer)
        if set(re.findall(r"[a-z']+", message.lower())) & {"bye", "goodbye", "quit", "exit"}:
            break
