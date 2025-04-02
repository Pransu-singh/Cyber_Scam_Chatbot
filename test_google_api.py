import requests

GOOGLE_API_KEY = "AIzaSyC9mFmE_j8ox00NI-qwxzYJiR8hqP-50QU"  # Replace with your actual API key
SAFE_BROWSING_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

test_url = "http://malware.testing.google.test/testing/malware/"  # Known unsafe test site

payload = {
    "client": {"clientId": "cybersecurity-chatbot", "clientVersion": "1.0"},
    "threatInfo": {
        "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
        "platformTypes": ["ANY_PLATFORM"],
        "threatEntryTypes": ["URL"],
        "threatEntries": [{"url": test_url}],
    },
}

response = requests.post(f"{SAFE_BROWSING_URL}?key={GOOGLE_API_KEY}", json=payload)

print("\n🔍 Google API Response:")
print(response.json())  # Should show "matches" if unsafe
