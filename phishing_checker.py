import re
import whois
import requests
from confusable_homoglyphs import confusables
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# List of well-known phishing targets
COMMON_TARGETS = ["google.com", "paypal.com", "amazon.com", "microsoft.com", "bankofamerica.com"]

def extract_domain(url):
    """Extracts the second-level domain (SLD) to avoid false positives."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Remove 'www.' if present
    domain = domain.replace("www.", "")

    # Extract second-level domain (e.g., "google.com" from "mail.google.com")
    domain_parts = domain.split(".")
    if len(domain_parts) > 2:
        domain = ".".join(domain_parts[-2:])  # Take the last two parts

    return domain

def is_homoglyph_attack(url):
    """Detect homoglyph attacks while avoiding false positives."""
    try:
        domain = extract_domain(url)

        # ✅ If domain is an exact match with a common site, it's safe
        if domain in COMMON_TARGETS:
            return "✅ Safe"

        # 🔍 Check if domain contains mixed scripts or is visually similar
        if confusables.is_mixed_script(domain) or confusables.is_confusable(domain):
            return f"⚠️ High Risk (Mimicking {domain})"

        return "✅ Safe"
    except Exception:
        return "⚠️ Error analyzing homoglyph risk"

def expand_shortened_url(url):
    """Expands shortened URLs by following redirects."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except requests.RequestException:
        return url

def get_whois_info(domain):
    """Fetches WHOIS info for a domain and returns domain creation date (age)."""
    try:
        domain_info = whois.whois(domain)

        if not domain_info or (isinstance(domain_info, str) and "No match" in domain_info):
            return "⚠️ Domain does not exist"

        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]  # Use the earliest date
        
        return str(creation_date) if creation_date else "⚠️ No creation date found"
    
    except whois.parser.PywhoisError:
        return "⚠️ WHOIS data restricted (Privacy protection enabled)"
    
    except Exception as e:
        return f"⚠️ WHOIS lookup failed: {str(e)}"

def analyze_page_content(url):
    """Analyzes website content for phishing indicators."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }  # Pretend to be a Chrome browser
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 403:
            return "⚠️ Access Denied (HTTP 403) – Website is blocking bots."

        if response.status_code != 200:
            return f"⚠️ Unable to fetch website (HTTP {response.status_code})"

        soup = BeautifulSoup(response.text, "html.parser")
        login_forms = soup.find_all("form", {"action": True})
        phishing_keywords = ["login", "verify", "security", "update", "bank", "password"]

        for form in login_forms:
            action_url = form["action"].lower()
            if any(keyword in action_url for keyword in phishing_keywords):
                return "⚠️ Warning: Suspicious login form detected!"

        return "✅ No immediate phishing indicators found."

    except requests.exceptions.ConnectionError:
        return "⚠️ Website does not exist or is currently unreachable."

    except requests.exceptions.Timeout:
        return "⚠️ Website took too long to respond (Timeout)."

    except requests.exceptions.RequestException as e:
        return f"⚠️ Unable to analyze website. Reason: {str(e)}"

def check_phishing(url):
    """Runs multiple phishing detection checks on a given URL."""
    url = expand_shortened_url(url)
    domain = re.sub(r"https?://(www\.)?", "", url).split('/')[0]

    result = {
        "URL": url,
        "Homoglyph Attack Risk": is_homoglyph_attack(url),
        "Domain Age": get_whois_info(domain),
        "Content Analysis": analyze_page_content(url)
    }
    
    return result  
