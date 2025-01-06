import json
import requests
import base64


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
    if tokenResponse.status_code == 200:
        tokenInfo = json.loads(tokenResponse.content)
        accessToken = tokenInfo["access_token"]
        print("Successful Request")
        return accessToken
    else:
        print("Unsuccessful request for access token, status code: {response.status_code}")
        print(tokenResponse.text)
        return None