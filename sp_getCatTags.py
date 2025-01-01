import requests

def getCatTags(accessToken = str):
    browseCatsURL = "https://api.spotify.com/v1/browse/categories"
    locale = "en_US"
    headers = {
        "Authorization": f"Bearer {accessToken}"
    }
    # make the get request
    catsResp = requests.get(browseCatsURL + "?" + "locale=" + locale, headers=headers)
    print(catsResp.text)
    # put categories in a list
    catTags = []
    for i in enumerate(catsResp.json()['categories']['items']):
        print(i[1]['name'])
        catTags.append(i[1]['name'])
    return catTags