from flask import Flask, render_template, request, jsonify
import re
import hashlib
import requests
#from flask_cors import CORS  # Required for handling cross-origin requests

app = Flask(__name__)
#CORS(app)  # Enable CORS for cross-origin frontend-backend communication

# Load passwords.txt for dictionary detection
def load_passwords():
    try:
        with open('passwords.txt', 'r', encoding='utf-8') as file:
            return set(line.strip().lower() for line in file)
    except FileNotFoundError:
        print("Warning: passwords.txt file not found. Using an empty password list.")
        return set()

COMMON_PASSWORDS = load_passwords()

# Password Strength Function
def check_password_strength(password):
    strength = 0
    if len(password) >= 8:
        strength += 1
    if any(char.isupper() for char in password):
        strength += 1
    if any(char.isdigit() for char in password):
        strength += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        strength += 1

    if strength == 4:
        return "Strong"
    elif strength == 3:
        return "Medium"
    else:
        return "Weak"

# Common Password Detection
def detect_common_passwords(password):
    if password.lower() in COMMON_PASSWORDS:
        return "Warning: Your password is listed in commonly used passwords. Avoid using it!"
    return "Your password is not listed in commonly used passwords."

# Check Password Breach (using Have I Been Pwned API)
def check_breach(password):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"  # Pass this URL to requests.get()
    try:
        response = requests.get(url, timeout=10)  # Fix: Include the 'url' argument
        response.raise_for_status()  # Raise HTTP error if response is not OK
        hashes = response.text.splitlines()  # Process the API response
        for line in hashes:
            hash_suffix, count = line.split(':')
            if suffix == hash_suffix:
                return f"This password has been found in {count} breaches. Avoid using it!"
        return "This password has not been found in any breaches. You're safe!"
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to check the password breach status. ({e})"
# Routes
@app.route('/')
def home():
    return render_template('index.html')  # Password Checker

@app.route('/generator')
def generator():
    return render_template('generator.html')  # Password Generator

@app.route('/about')
def about():
    return render_template('about.html')  # About Page

@app.route('/check-live', methods=['POST'])
def check_live():
    data = request.get_json()
    password = data.get('password', '')

    strength = check_password_strength(password)
    common_password_warning = detect_common_passwords(password)

    return jsonify({
        "strength": strength,
        "dictionary_warning": common_password_warning
    })

@app.route('/check-breach', methods=['POST'])
def check_breach_endpoint():
    data = request.get_json()
    password = data.get('password', '')
    breach_status = check_breach(password)  # Ensure this function works correctly
    return jsonify({"breach_status": breach_status})

if __name__ == '__main__':
    app.run(debug=True)