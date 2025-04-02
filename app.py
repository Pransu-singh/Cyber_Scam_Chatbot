import os
import requests
import wikipediaapi
from flask import Flask, request, jsonify, render_template, Response, stream_with_context
import ollama
from dotenv import load_dotenv
import json
import re
import base64

from phishing_checker import check_phishing
from password_checker import check_password_strength

load_dotenv()
app = Flask(__name__)

# Use environment variables for sensitive data
GOOGLE_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")
print("Loaded API Key:", GOOGLE_API_KEY) 
SAFE_BROWSING_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")  # Load API key from .env
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/urls"



# Predefined knowledge base for quick answers
knowledge_base = {
    "what is cyber security": "Cybersecurity is the practice of protecting systems, networks, and data from digital attacks.",
    "how to stay safe online": "Use strong passwords, enable 2FA, avoid phishing emails, and keep your software updated.",
    "check website ": "Please enter a valid URL to check its safety."}
def get_wikipedia_summary(query):
    """Fetches a short summary from Wikipedia."""
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(query)

    if page.exists():
        return page.summary[:300] + "..."
    return "I couldn't find relevant information on Wikipedia."

def check_website_safety(url):
    """Checks if a website is safe using both Google Safe Browsing API and VirusTotal API."""
    
    # Check with Google Safe Browsing
    google_result = check_google_safe_browsing(url)
    
    # Check with VirusTotal
    virustotal_result = check_virustotal(url)

    return f"🔍 Google Safe Browsing Result:\n{google_result}\n\n🛡️ VirusTotal Result:\n{virustotal_result}"


def check_google_safe_browsing(url):
    """Checks if a website is safe using Google Safe Browsing API."""
    
    if not GOOGLE_API_KEY:
        return "⚠️ API key missing! Please set up the Google Safe Browsing API key."
    
    payload = {
        "client": {"clientId": "cybersecurity-chatbot", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": [
                "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION", "THREAT_TYPE_UNSPECIFIED"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    
    try:
        response = requests.post(f"{SAFE_BROWSING_URL}?key={GOOGLE_API_KEY}", json=payload)
        data = response.json()
        
        if "matches" in data and data["matches"]:
            return f"🚨 Warning: The website {url} is unsafe! (Detected as {data['matches'][0]['threatType']})"
        else:
            return f"✅ The website {url} appears safe in Google's database (no recorded threats)."
    
    except requests.exceptions.RequestException as e:
        return f"❌ Google Safe Browsing Error: {str(e)}"

def check_virustotal(url):
    """Checks if a website is safe using VirusTotal API."""
    
    if not VIRUSTOTAL_API_KEY:
        return "⚠️ API key missing! Please set up the VirusTotal API key."
    
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY,
    }
    
    # Step 1: Check if the URL already has a report in VirusTotal
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")  # Encode URL to match VirusTotal format
    report_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    
    try:
        report_response = requests.get(report_url, headers=headers)
        if report_response.status_code == 200:
            report_data = report_response.json()
            stats = report_data.get("data", {}).get("attributes", {}).get("stats", {})
            malicious_count = stats.get("malicious", 0)
            suspicious_count = stats.get("suspicious", 0)
            
            if malicious_count > 0 or suspicious_count > 0:
                return f"🚨 Warning: VirusTotal detected {malicious_count} malicious & {suspicious_count} suspicious reports for {url}!"
            else:
                return f"✅ The website {url} appears safe on VirusTotal (no reported threats)."
        
        # Step 2: If no report is found, submit URL for scanning
        submit_response = requests.post(VIRUSTOTAL_URL, headers=headers, data={"url": url})
        if submit_response.status_code == 200:
            return f"🔄 VirusTotal is scanning {url}. Try again later for updated results."
        else:
            return f"❌ VirusTotal Error: {submit_response.status_code} - {submit_response.text}"

    except requests.exceptions.RequestException as e:
        return f"❌ VirusTotal Error: {str(e)}"



def extract_url(text):
    """Extract the first URL from user input, regardless of surrounding text."""
    url_pattern = re.compile(r"https?://[^\s]+", re.IGNORECASE)
    match = url_pattern.search(text)
    return match.group() if match else None

def generate_chat_response(user_message):
    """Handles general chatbot messages."""
    responses = {
        "help": "🔍 I can check website safety. Just send me a URL.",
        "bye": "👋 Goodbye! Stay safe!"
    }
    return responses.get(user_message, "🤖 Sorry, I don’t understand. Try again!")

def get_ai_response_stream(user_message):
    """Generator function to stream response from Ollama."""
    for chunk in ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": user_message}], stream=True):
        yield chunk['message']['content'] + " "
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()
    
    # Check if the message contains a URL
    extracted_url = extract_url(user_message)
    
    
    
    
    # Check password strength
    if "check password" in user_message or "password strength" in user_message:
        password = user_message.replace("check password", "").replace("password strength", "").strip()
        if password:
            result = check_password_strength(password)
            return jsonify(result)
        return jsonify({"error": "Please provide a password to check."})

    # Default AI Response
        return jsonify({"response": "🤖 I don’t understand. Try again!"})
    
    if extracted_url:
        response_text = check_website_safety(extracted_url)
        return Response(response_text, content_type="text/plain; charset=utf-8")

    # Quick response from the knowledge base
    if user_message in knowledge_base:
        return Response(knowledge_base[user_message], content_type="text/plain; charset=utf-8")

    # Wikipedia Lookup
    if user_message.startswith("wiki "):
        query = user_message.replace("wiki ", "").strip()
        wiki_summary = get_wikipedia_summary(query)
        return Response(wiki_summary, content_type="text/plain; charset=utf-8")
    # AI Response Streaming
    return Response(
        stream_with_context(get_ai_response_stream(user_message)), 
        content_type="text/plain; charset=utf-8"
    )
@app.route("/check-phishing", methods=["POST"])
def phishing_check():
    url = request.json.get("url")
    result = check_phishing(url)
    return jsonify(result)

@app.route("/check-password", methods=["POST"])
def password_check():
    password = request.json.get("password")
    result = check_password_strength(password)
    return jsonify(result)
if __name__ == "__main__":
    app.run(debug=True)
