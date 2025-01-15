from sp_getAccessToken import getAccessToken
import sp_getPlaylistInfo as pInfo
import sp_getTrackInfo as tInfo
from sp_search import search
from dotenv import load_dotenv
from os import getenv
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()
clientID = getenv("clientID")
clientSecret = getenv("clientSecret")

accessToken = getAccessToken(clientID, clientSecret)

searchTerms = [
    'Chinese||Mandarin', 
    'Philipino||Tagalog', 
    'French', 
    'arabi||Arabic', 
    'Korean', 
    'Russian', 
    'German', 
    'American',
    'spanish||espanol||hispanic', 
    "baladi",
    "In English",
    "Reggaeton",
    "Salsa",
    "Gaelic",
    "bollywood",
    "hindi", 
    "Persian", 
    "Urdu",
    "Vietnamese",
    "Bhangra",
    "Panjabi||Punjabi",
    "Japanese",
    "German", 
    "Portuguese",
    "Phonk",
    "Fado",
    "Reggae",
    "Anime",
    "Latin",
    "Samba",
    "Middle Eastern",
    "Nordic",
    "Afrobeat",
    "karnatic"
]


# THIS SECTION IS LOOKING AT AVERAGE FOLLOWERS OF SEARCHTERM-SPECIFIC PLAYLISTS AND THEIR CONTAINED TRACKS' AVERAGE POPULARITY
""" compiledDict = {'Search Term': [], 'Avg Followers': [], 'Avg Playlist Popularity': []}

for i in range(0, len(searchTerms)):
    print(f"================ THIS IS RUN {i}===================")
    limit = 3
    response = search(searchTerms[i], limit, "playlist", "US", accessToken)
    if response['playlists'] and response['playlists']['items']:
        playlistID = pInfo.getPlaylistIDFromSearch(response) #returns a list # return to inputting response if inputting cleanedResponse doesn't work
        print("Playlist ID List: ")
        print(playlistID)
        playlistDict = {'PlaylistID': [], 'AvgPopularity': [], 'Followers': []}
        for j in playlistID:
            avgPop = pInfo.getPlaylistItemsPopularity(j, 'US', accessToken) # CURRENTLY THROWING THE "NONE TYPE OBJECT IS NOT SUBSCRIPTABLE" ERROR
            playlistDict["PlaylistID"].append(j)
            playlistDict["AvgPopularity"].append(avgPop)
            playlistDict["Followers"].append(pInfo.getFollowers(accessToken=accessToken, playListID=j))

        searchTermDf = pd.DataFrame.from_dict(playlistDict)
        
        avgFollowersForSearchTerm = searchTermDf['Followers'].mean()
        avgPopForSearchTerm = searchTermDf['AvgPopularity'].mean()

        print("============================================")
        print(f"For search term '{searchTerms[i]}', avg follower count of {limit} playlists \n is {avgFollowersForSearchTerm} and avg popularity of the songs on these playlists\n is {avgPopForSearchTerm}")
        compiledDict['Search Term'].append(searchTerms[i])
        compiledDict['Avg Followers'].append(avgFollowersForSearchTerm)
        compiledDict['Avg Playlist Popularity'].append(avgPopForSearchTerm)
        print(compiledDict)

        
    if None in response:
        print("None found in search results")
        continue
    if response is None or not response.get('playlists', {}).get('items'):
        print("No playlists returned for this search term")
        continue

data = pd.DataFrame.from_dict(compiledDict)
data.plot.bar(x='Search Term', y='Avg Followers')
plt.show() """


response = search(searchTerms[0], 1, "playlist", "US", accessToken)
playlistIDList = pInfo.getPlaylistIDFromSearch(response)
popularity = pInfo.getPlaylistItemsPopularity(playlistID=playlistIDList[0], market='US', accessToken=accessToken)
print("Popularity = " + str(popularity))
tracks = tInfo.getPlaylistItems(playlistId=playlistIDList[0], accessToken=accessToken)
# for songname, artistname in tracks['trackname'], tracks['artistname']:
for songid in tracks['trackid']:
    idx = tracks['trackid'].index(songid)
    songname = tracks['trackname'][idx]
    artistname = tracks['artistname'][idx]
    print(tInfo.getLyricsLanguage(songname, artistname))


tInfo.getTrackArtistGenre(tracks['artistid'][0:5], accessToken)