import requests

'''will search spotify based on a search string, limit the results by an int, search by artist, 
playlist, track, or album, search by country code (two characters), and requires an access token'''
def search(searchstr = str, resultsLim = int, searchType = str, country = str, accessToken = str):
    searchListURL = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {accessToken}"
    }
    query = f"?q={searchstr}&type={searchType}&market={country}&limit={resultsLim}"
    searchResponse = requests.get(searchListURL + query, headers=headers)
    return searchResponse