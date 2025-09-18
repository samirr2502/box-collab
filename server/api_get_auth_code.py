import requests
import json
import os
import webbrowser
# Load config once
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "serverconfig.json")

with open(file_path) as f:
    config = json.load(f)
CLIENT_SECRET = config["CLIENT_SECRET"]

def main():
    CLIENT_ID = config["CLIENT_ID"]

    REDIRECT_URI = config["REDIRECT_URI"]


    auth_code_url = f"https://account.box.com/api/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"


    response = requests.get(auth_code_url)
    webbrowser.open(auth_code_url)

    #auth_code_response = response.json()

    #auth_code_ = auth_code_response.get("code")

    print(f"Response: {response}")
