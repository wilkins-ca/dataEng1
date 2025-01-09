from sp_getAccessToken import getAccessToken
import sp_getPlaylistInfo as pInfo
from sp_search import search
from dotenv import load_dotenv
from os import getenv

load_dotenv()
clientID = getenv("clientID")
clientSecret = getenv("clientSecret")
langs = getenv("langs")
print(langs)

accessToken = getAccessToken(clientID, clientSecret)
print("Access token = " + accessToken)

response = search("spanish||hispanic", 2, "playlist", "US", accessToken)
playlistID = pInfo.getPlaylistIDFromSearch(response) #returns a list
print(playlistID)
playlistDict = {'PlaylistID': [], 'AvgPopularity': [], 'Followers': []}
for i in playlistID:
    print("Playlist ID = " + i + ". Type = " + str(type(i)))
    avgPop = pInfo.getPlaylistItemsPopularity(i, 'US', accessToken)
    playlistDict["PlaylistID"].append(i)
    playlistDict["AvgPopularity"].append(avgPop)
    playlistDict["Followers"].append(pInfo.getFollowers(accessToken=accessToken, playListID=i))
print(playlistDict)