from numpy import average
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
    "Egyptian",
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
    "karnatic",
    "celtic"
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


for i in searchTerms[0:1]:
    response = search(i, 1, "playlist", "US", accessToken)
    playlistIDList = pInfo.getPlaylistIDFromSearch(response)
    for playlist in playlistIDList:
        popularity = pInfo.getPlaylistItemsPopularity(playlistID=playlist, market='US', accessToken=accessToken)
        tracks = tInfo.getPlaylistItems(playlistId=playlist, accessToken=accessToken)
        df = pd.DataFrame(tracks)
        df.to_csv("trackInfo.csv")



""" popPerTerm = {"SearchTermUsed": [], "avgPopularity": []}
for j in searchTerms: #start off with just one search term until things look good
    print(f"Current Search Term is {j}")
    limit = 50 # we want the top 100 artists in the US
    topArtists = {"name": [], "id": [], "popularity": [], "SearchTermUsed": []}
    response1 = search(j, limit, "artist", accessToken=accessToken) #search for artists
    for artist in response1['artists']['items']:
        if artist['id'] not in enumerate(topArtists["id"]): #if the artist id in search results in not in the artist ids in our established topArtists 
            #append info to the topartists dict
                topArtists["name"].append(artist['name'])
                topArtists["id"].append(artist['id'])
                topArtists["popularity"].append(artist['popularity'])
                topArtists["SearchTermUsed"].append(j)

        if len(topArtists) >= limit: #if we've reached the limit, exit the loop
            break
    avgPop = average(topArtists["popularity"]) #compute average popularity between 50 artists returned from the search term
    popPerTerm["avgPopularity"].append(avgPop)
    popPerTerm["SearchTermUsed"].append(j)

topArtists["popularity"] = sorted(topArtists["popularity"], reverse = True) #sort by popularity in descending order for the whole of the topArtists list

popInfo = pd.DataFrame(popPerTerm)
print(popInfo)
fig, axes = plt.subplots(figsize=(8, 10))
axes.barh(popInfo["SearchTermUsed"], popInfo["avgPopularity"], color="skyblue")
# axes.tick_params(axis='x', which="major", pad=10, labelsize=9, rotation=45)
axes.set_ylabel("Search Term Used\nNote: it is recognized that some of the artist\nresults may not be directly related to the search term by language correlation")
axes.set_xlabel("Avg Popularity Rank across 50 artists")
plt.tight_layout()
plt.show() """