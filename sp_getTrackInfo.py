import requests
from languagedetect import detectLanguage
from lyricsgenius import Genius
from dotenv import load_dotenv
from os import getenv

load_dotenv()
geniusAccessToken = getenv("geniusAccessToken")

'''will collect the artist and track information for each song given a playlist ID'''
def getPlaylistItems(playlistId = str, accessToken = str):
    if not accessToken: # make sure access token is there
        print(f"Access token isn't here: {accessToken}")
        return None
    headers = { #set up headers
        "Authorization": f"Bearer {accessToken}"
    }

    url = "https://api.spotify.com/v1/playlists/" + playlistId + "/tracks" #get playlist's tracks endpoint

    resp = requests.get(url, headers = headers) #make the api call

    trackInfoDict = {"trackid": [], "trackname": [], "popularity": [], "artistid": [], "artistname": []} #set up dictionary to be returned 
    if resp.status_code == 200: # check success of the request
        print("Successful Request of get Playlist Items Endpoint")
        tracks = resp.json()['items'] # pull bulk track info
        for i in tracks: #check if the track is actually there
            if i:
                #add track info to dict, track ID, name, popularity, and track's artist ID
                trackInfoDict['trackid'].append(i['track']['id'])
                trackInfoDict["trackname"].append(i['track']['name'])
                trackInfoDict["artistid"].append(i['track']['artists'][0]['id'])
                trackInfoDict["popularity"].append(i['track']['popularity'])
                trackInfoDict["artistname"].append(i['track']['artists'][0]['name'])
            else:
                print("Null track, continuing") #go to next iteration of the loop if track is not there
                continue
        return trackInfoDict
    else: #more error checking
        print(f"Unsuccessful Request to get playlist items: status_code = " + str(resp.status_code) + " and resp.text = " + resp.text)
        return None
    

'''will make a dict of artist's genres and artist ID, must pass list of artist IDs'''
def getTrackArtistGenre(trackInfoList, accessToken = str):
    headers = { #set up headers
        "Authorization": f"Bearer {accessToken}"
    }
    url = "https://api.spotify.com/v1/artists/" #artist info endpoint

    #establish list of dicts to hold artist IDs and corresponding genres which is to be returned
    artistInfo = []
    for artistid in trackInfoList:
        #make request to get artist info endpoint
        response = requests.get(url=url + artistid, headers=headers)

        #extract genres
        genres = response.json()['genres']
        #add genres and IDs to list of dicts
        tempdict = {'Artist ID': artistid, 'Genres': genres}
        artistInfo.append(tempdict)
    
    return artistInfo



'''function to extract the language of the given track's lyrics; input should be strings of Artist Name and 
Track Name'''
def getLyricsLanguage(trackname = str, artistname = str):
    genius = Genius(geniusAccessToken)
    track = genius.search_song(trackname, artistname)
    #get the particular song info plus error checking
    if track:
        lang = detectLanguage(track.lyrics) #use detectLanguage function to return English name of lyrics' language
        return lang
    else:
        print("Track not there")
        return None