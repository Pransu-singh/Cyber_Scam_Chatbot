import requests
import wikipediaapi
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify,render_template
import ollama

app = Flask(__name__)

# Rule-Based Knowledge Base
knowledge_base = {
    "what is cyber security": "Cybersecurity is the practice of protecting systems, networks, and data from digital attacks.",
    "how to stay safe online": "Use strong passwords, enable 2FA, avoid phishing emails, and keep your software updated."
}

# Wikipedia Summary Function
def get_wikipedia_summary(query):
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(query)
    if page.exists():
        return page.summary[:300]  # Return first 300 characters
    return "I couldn't find relevant information."

# Web Scraping from Google (Basic)
def search_google(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    snippets = soup.find_all("span")
    for snippet in snippets:
        if snippet.text and len(snippet.text) > 50:
            return snippet.text
    return "I couldn't find a good answer."

# Function to Get AI Response from Ollama (Gemma 2B)
def get_ai_response(user_message):
    response = ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": user_message}])
    return response["message"]["content"]
@app.route("/")
def home():
    return render_template("index.html") 


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower().strip()

    # 1️⃣ Rule-Based Response
    if user_message in knowledge_base:
        return jsonify({"response": knowledge_base[user_message]})

    # 2️⃣ AI Model Response (Ollama)
    ai_response = get_ai_response(user_message)

    # 3️⃣ Web Scraping (if AI Model is unsure)
    if "I don't know" in ai_response.lower():
        web_response = get_wikipedia_summary(user_message)
        return jsonify({"response": web_response})

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
