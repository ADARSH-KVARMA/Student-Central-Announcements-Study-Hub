import requests

# Replace this with your actual deployed Apps Script URL
YOUR_DEPLOYMENT_ID = "AKfycbxreQycF3Amnn7QxH27v6ZrsulGvclAzqLG1LsTbiot2Ma4puwzCvdNV3BNLXhVu8mU"
WEB_APP_URL = f"https://script.google.com/macros/s/{YOUR_DEPLOYMENT_ID}/exec"

def get_users():
    try:
        response = requests.get(WEB_APP_URL)
        response.raise_for_status()
        data = response.json()
        headers = data[0]
        users = [dict(zip(headers, row)) for row in data[1:]]
        return users
    except Exception as e:
        print("Error getting users:", e)
        return []

def register_user(username, password):
    try:
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(WEB_APP_URL, json=payload)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("Error registering user:", e)
        return "Failed"
