
# 🛡️ Cybersecurity Chatbot

An intelligent, hybrid-model cybersecurity chatbot built using a combination of AI (local LLM via Ollama), rule-based logic, and web scraping techniques. Designed to assist users in identifying phishing links, checking website safety, and evaluating password strength — all in real-time with privacy-focused tools and APIs.

---

## 🚀 Features

- 🔍 **Fake Link & Phishing Detection**
  - Homoglyph detection (e.g., `g00gle.com` vs `google.com`)
  - Shortened URL expansion and analysis
  - WHOIS record inspection
  - Content-based phishing heuristics

- 🔐 **Password Strength Checker**
  - Regex and entropy-based analysis
  - Breach database check (using HaveIBeenPwned or local dataset)

- 🌐 **Website Safety Checker**
  - Google Safe Browsing API integration
  - VirusTotal API analysis

- 🤖 **Hybrid AI Model**
  - Local LLM using [Ollama](https://ollama.com/)
  - Rule-based responses for quick decisions
  - Web scraping for up-to-date threat intelligence

- 🧠 **Smart Query Understanding**
  - Natural language understanding for user questions
  - Context-aware responses

---

## 🛠️ Tech Stack

| Layer          | Technology                           |
|----------------|--------------------------------------|
| Frontend       | HTML, CSS, JavaScript                |
| Backend        | Python (Flask / FastAPI)             |
| AI/LLM         | Open-source LLM via Ollama           |
| APIs Used      | Google Safe Browsing, VirusTotal, HaveIBeenPwned |
| Web Scraping   | BeautifulSoup, requests              |

---

## 📂 Project Structure

```

cybersecurity-chatbot/
│
├── backend/
│   ├── app.py
│   ├── phishing\_detector.py
│   ├── password\_checker.py
│   ├── website\_checker.py
│   └── utils/
│       └── helpers.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── static/
│
├── templates/
│
├── requirements.txt
└── README.md

````

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cybersecurity-chatbot.git
cd cybersecurity-chatbot
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Ollama with a Local LLM

Make sure [Ollama](https://ollama.com) is installed and running a model like `llama2`:

```bash
ollama run llama2
```

### 5. Start the Backend

```bash
python backend/app.py
```

### 6. Open in Browser

Open `frontend/index.html` in your browser.

---

## 🔒 API Key Setup (Optional for Full Functionality)

Create a `.env` file in the backend directory and add:

```
GOOGLE_SAFE_BROWSING_API_KEY=your_key_here
VIRUSTOTAL_API_KEY=your_key_here
HIBP_API_KEY=your_key_here  # If using HaveIBeenPwned API
```

 

## 📜 License

This project is open-source under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests to add features or report bugs.

---

## 📧 Contact

* Developer: Pransu Singh
* Email: singhpransu22@gmail.com
* GitHub: @pransu-singh
 
