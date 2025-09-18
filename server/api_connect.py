import requests
import time
import json
import os

# Load config once
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "serverconfig.json")

with open(file_path) as f:
    config = json.load(f)
CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]


AUTH_CODE = ''
ACCESS_TOKEN = ''
REFRESH_TOKEN =''
DEV_TOKEN =config["DEV_TOKEN"]
REDIRECT_URI = config["REDIRECT_URI"]
token_url = "https://api.box.com/oauth2/token"

#print(f'authcode: {AUTH_CODE}\n')


def get_access_token(code):
    AUTH_CODE = code
    #Uncomment the following line to use DEV_TOKEN
    #AUTH_CODE = DEV_TOKEN
    data_token = {
        "grant_type": "authorization_code",
        "code": AUTH_CODE,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(token_url, data=data_token)
    tokens = response.json()

    ACCESS_TOKEN = tokens.get("access_token")
    REFRESH_TOKEN = tokens.get("refresh_token")

    # print(f"Access Token: {access_token}")
    # print(f"Refresh Token: {refresh_token}")
    return ACCESS_TOKEN, REFRESH_TOKEN

def refresh_token(refresh_token):
    # Request body
    print("attempting to refresh token after 10 seconds")
    data_refresh = {
    "grant_type": "refresh_token",
    "refresh_token": refresh_token,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=data_refresh, headers=headers)
    if response.status_code == 200:
        tokens = response.json()
        ACCESS_TOKEN = tokens["access_token"]
        REFRESH_TOKEN = tokens["refresh_token"]
        print("Token refreshed successfully.")
    else:
        print("Failed to refresh token:", response.json())
    return ACCESS_TOKEN, REFRESH_TOKEN
        
def handle_box_exception(file,e):

    print(f"Failed to run box api: HTTP {e.status} - {e.message} - {e.getResponse}\n")
    file.write(f"Failed to run box api: HTTP {e.status} - {e.message}\n")
    file.flush()
    if e.status == 404:
        print("Folder not found!\n")
        file.write("Folder not found!\n")
        print("Trying to refresh token!\n")
        file.write("Trying to refresh token!\n")
        refresh_token(REFRESH_TOKEN)
    elif e.status == 401:
        print("No permissions [refresh token might have failed]")
    elif e.status == 403:
        print("No permission to access this folder!\n")
        file.write("No permission to access this folder!\n")
    elif e.status == 429:
        print("Rate limit exceeded! Try again later\n.")
        file.write("Rate limit exceeded! Try again later\n.")
