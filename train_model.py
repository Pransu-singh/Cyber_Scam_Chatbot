import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training Data - Add More Variations!
questions = [
    "what is cybersecurity", "how to stay safe online", "what is a firewall",
    "explain phishing", "how to protect my password", "what is malware",
    "hii", "hello", "hi", "hey", "hlo", "good morning", "good evening",
    "who are you", "what can you do", "how does a firewall work",
    "explain ransomware", "tell me about trojans", "how do hackers attack",
    "how to report cybercrime", "what is ethical hacking", "how to secure my wifi"
]
answers = [
    "Cybersecurity is protecting systems and networks from cyber threats.",
    "Use strong passwords, enable 2FA, and avoid suspicious links.",
    "A firewall monitors and controls incoming and outgoing network traffic.",
    "Phishing is a cyber attack where attackers trick you into giving sensitive info.",
    "Use strong, unique passwords and enable 2FA.",
    "Malware is a type of software designed to harm or exploit devices.",
    "Hello! How can I help you today?",
    "Hey! Need any cybersecurity help?",
    "Hello! I'm here to assist you with cybersecurity questions.",
    "Hi there! Ask me anything about cybersecurity.",
    "Hey! I'm your cybersecurity assistant.",
    "Good morning! How can I help?",
    "Good evening! Need any cybersecurity tips?",
    "I am a cybersecurity chatbot designed to help you stay safe online.",
    "I can answer cybersecurity questions, detect threats, and provide guidance.",
    "Firewalls filter traffic to prevent unauthorized access.",
    "Ransomware locks your files and demands payment to unlock them.",
    "Trojans disguise themselves as legitimate software to steal your data.",
    "Hackers use phishing, malware, and other methods to attack systems.",
    "You can report cybercrime to local authorities or CERT.",
    "Ethical hacking involves testing security systems to find vulnerabilities.",
    "To secure your WiFi, use WPA2 encryption, strong passwords, and hide SSID."
]

# Train Model
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(questions)
model = MultinomialNB()
model.fit(X_train, answers)

# Save Model & Vectorizer
with open("chatbot_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("✅ Model Trained and Saved Successfully!")
