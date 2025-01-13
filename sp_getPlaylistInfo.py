from numpy import ceil
import requests

''' will pull the playlist IDs from search results'''
def getPlaylistIDFromSearch(searchResults):
    playlistIDList = []
    items = searchResults.get('playlists', {}).get('items')
    for i in items:
        print(type(i))
        print("i in get Playlist ID from Search == ")
        print(i)
        if not i['id']:
            print("No playlist ID found")
        else:
            playlistIDList.append(i['id'])
    return playlistIDList


'''calculates the average popularity of the tracks in the given playlist, rounded up to the next whole number.
market = country code'''
def getPlaylistItemsPopularity(playlistID = str, market = str, accessToken = str):
    if not accessToken:
        print(f"Access token isn't here: {accessToken}")
        return None
    headers = {
        "Authorization": f"Bearer {accessToken}"
    }

    url = "https://api.spotify.com/v1/playlists/" + playlistID + "/tracks?" + "market=" + market
    resp = requests.get(url, headers = headers)
    if resp.status_code == 200: # check success of the request
        print("Successful Request of get Playlist Items Endpoint")
        tracks = resp.json()['items'] # pull bulk track info
        sumOfPop = 0
        count = 0
        for i in enumerate(tracks): # begin calculating avg 
            sumOfPop += i[1]['track']['popularity']
            count += 1
        
        popularity = ceil(sumOfPop / count) # actual avg calc 
        return popularity
    else: #if not successful
        print(f"Unsuccessful Request to get playlist items: status_code = " + str(resp.status_code) + " and resp.text = " + resp.text)
        return None


'''will pull the total followers of the playlist'''
def getFollowers(accessToken = str, playListID = str):
    url = "https://api.spotify.com/v1/playlists/" + playListID
    headers = {
        "Authorization": f"Bearer {accessToken}"
    }
    resp = requests.get(url, headers = headers)
    if resp.status_code == 200:
        print("Successful Request to Get Followers")
        playlistInfo = resp.json()
        followers = playlistInfo['followers']['total']
        return int(followers)
    else:
        print(f"Unsuccessful Request to get Followers: status code {resp.status_code}. Resp.text = {resp.text}")
        return None