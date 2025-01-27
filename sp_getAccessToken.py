import requests
import base64
from datetime import datetime, timedelta

accessToken = None
tokenExpiryTime = None

def getAccessToken(clientID = str, clientSecret = str):
    tokenURL = "https://accounts.spotify.com/api/token"
    client = f"{clientID}:{clientSecret}"
    authbytes = client.encode("utf-8")
    encodedClient = str(base64.b64encode(authbytes), "utf-8")
    accessTokenHeaders = {
        "Authorization": f"Basic {encodedClient}",
        "Content-Type":"application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    tokenResponse = requests.post(tokenURL, headers=accessTokenHeaders, data=data)
    if tokenResponse.get("access_token"):
        global tokenExpiryTime
        tokenExpiryTime = datetime.now() + timedelta(seconds = tokenResponse["expires_in"])
        return accessToken
    else:
        print("Unsuccessful request for access token, status code: {response.status_code}")
        print(tokenResponse.text)
    

def isTokenValid():
    global tokenExpiryTime
    # check if token is stil valid
    return tokenExpiryTime and datetime.now() < tokenExpiryTime