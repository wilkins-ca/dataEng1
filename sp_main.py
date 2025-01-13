from sp_getAccessToken import getAccessToken
import sp_getPlaylistInfo as pInfo
from sp_search import search
from dotenv import load_dotenv
from os import getenv
from pandas import DataFrame as df

load_dotenv()
clientID = getenv("clientID")
clientSecret = getenv("clientSecret")
langs = getenv("langs")
print(langs)

accessToken = getAccessToken(clientID, clientSecret)

searchTerms = [
    'spanish||hispanic',
    'english',
    'Chinese||Mandarin||Cantonese', 
    'Philipino||Tagalog', 
    'French', 
    'arabi||Arabic', 
    'Korean', 
    'Russian', 
    'German'
]

""" firstSearchTerm = searchTerms[0]
limit = 20
response = search(firstSearchTerm, limit, "playlist", "US", accessToken) # eventually for each search term, we want to sum metrics across playlists and take average
playlistID = pInfo.getPlaylistIDFromSearch(response) #returns a list
print(playlistID)
playlistDict = {'PlaylistID': [], 'AvgPopularity': [], 'Followers': []}
for i in playlistID:
    avgPop = pInfo.getPlaylistItemsPopularity(i, 'US', accessToken)
    playlistDict["PlaylistID"].append(i)
    playlistDict["AvgPopularity"].append(avgPop)
    playlistDict["Followers"].append(pInfo.getFollowers(accessToken=accessToken, playListID=i))

searchTermDf = df.from_dict(playlistDict)
compiledDict = {'Search Term': [], 'Avg Followers': [], 'Avg Playlist Popularity': []}
avgFollowersForSearchTerm = searchTermDf['Followers'].mean()
avgPopForSearchTerm = searchTermDf['AvgPopularity'].mean()

print(f"For search term '{firstSearchTerm}', avg follower count of {limit} playlists \n is {avgFollowersForSearchTerm} and avg popularity of the songs on these playlists\n is {avgPopForSearchTerm}") """
compiledDict = {'Search Term': [], 'Avg Followers': [], 'Avg Playlist Popularity': []}

for i in range(0, 2):
    print(f"================ THIS IS RUN {i}===================")
    limit = 2
    response = search(searchTerms[i], limit, "playlist", "US", accessToken)
    if response is None or not response.get('playlists', {}).get('items'):
        print("No playlists returned for this search term")
        continue
    playlistID = pInfo.getPlaylistIDFromSearch(response) #returns a list
    print("Playlist ID List: ")
    print(playlistID)
    playlistDict = {'PlaylistID': [], 'AvgPopularity': [], 'Followers': []}
    for j in playlistID:
        avgPop = pInfo.getPlaylistItemsPopularity(j, 'US', accessToken)
        playlistDict["PlaylistID"].append(j)
        playlistDict["AvgPopularity"].append(avgPop)
        playlistDict["Followers"].append(pInfo.getFollowers(accessToken=accessToken, playListID=j))

    searchTermDf = df.from_dict(playlistDict)
    
    avgFollowersForSearchTerm = searchTermDf['Followers'].mean()
    avgPopForSearchTerm = searchTermDf['AvgPopularity'].mean()

    print("============================================")
    print(f"For search term '{searchTerms[i]}', avg follower count of {limit} playlists \n is {avgFollowersForSearchTerm} and avg popularity of the songs on these playlists\n is {avgPopForSearchTerm}")
    compiledDict['Search Term'].append(searchTerms[i])
    compiledDict['Avg Followers'].append(avgFollowersForSearchTerm)
    compiledDict['Avg Playlist Popularity'].append(avgPopForSearchTerm)
    print(compiledDict)