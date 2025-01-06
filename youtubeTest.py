import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from os import getenv
import csv, time


genres = ['classical', 'pop', 'blues', 'rock', 'metal', 'reggaeton', 'hip hop', 'rap', 'traditional', 
          'folk', 'indie', 'r&b', 'electronic', 'country', 'funk']



apiServiceName = "youtube"
version = "v3"
load_dotenv()
apiKey = getenv("ytAPIkey")

youtube = build(apiServiceName, version, developerKey=apiKey)

#search by keyword, where search type is "video" or "playlist"
def search(youtube, keyword = str, maxResults = int, searchType = str):
    request = youtube.search().list(part = "snippet", maxResults = maxResults, q = keyword, type = searchType)
    return request.execute()

def getVidInfofromSearchResults(searchResults):
    vidInfo = []
    # add video id and title to list of dicts
    for i in enumerate(searchResults["items"]):
        tempdict = {"id": i[1]['id']['videoId'], "Title": i[1]['snippet']['title']}
        vidInfo.append(tempdict)
    return vidInfo


def getPlaylistIDFromSearch(searchResults):
    ids = []
    for i in enumerate(searchResults['items']):
        playlistdict = {'id': i[1]['id']['playlistId'], 'Title': i[1]['snippet']['title']}
        ids.append(playlistdict)
    return ids



def getPlaylistVids(playlistIDS):
    videoList = []

    for i in playlistIDS:
        nextPageToken = None
        while True:

            try:
                resp = youtube.playlistItems().list(part = 'snippet', playlistId = i['id'], 
                                                    maxResults = 50, pageToken = nextPageToken).execute()

                nextPageToken = resp.get('nextPageToken')
                if nextPageToken:
                    print("Next Page Token = " + nextPageToken)
                else:
                    print("No more pages to process in this playlist \n")
                
                for j in resp['items']:
                    vidID = j['snippet']['resourceId']['videoId']
                    title = j['snippet']['title']
                    videoList.append({'vidId': vidID, 'title': title, 'playlistID': i})
                
                if not nextPageToken:
                    print("Finished Processing playlist")
                    break
            except Exception as e:
                print(f"Error processing playlist {i}: {e}")
                break

    return videoList


def getVidStats(vidList):
    stats = []
    for i in range(0, len(vidList), 50):
        videoIDS = [video['vidId'] for video in vidList[i:i+50]]
        resp = youtube.videos().list(
            part = "statistics",
            id = ",".join(videoIDS)
        ).execute()

        for item in resp['items']:
            vidInfo = next(video for video in vidList if video['vidId'] == item['id'])
            stats.append({
                'id': item['id'],
                'title': vidInfo['title'],
                'playlistID': vidInfo['playlistID'], 
                'viewCount': int(item['statistics'].get('viewCount', 0)),
                'likeCount': int(item['statistics'].get('likeCount', 0)), 
                'commentCount': int(item['statistics'].get('commentCount', 0))
            })
    
    return stats

'''vidData is a list, searchterm is whatever genre tag was used for that particular 
api call '''
def logVidData(vidData, filename = "metrics.csv", searchTerm = str):
    with open(filename, 'a', newline = '', encoding = 'utf-8') as file:
        writer = csv.writer(file)
        for vid in vidData:
            writer.writerow([searchTerm, vid['id'], vid['title'], vid['viewCount'], vid['likeCount'], vid['commentCount'], time.time()])
            


'''
regularly poll the api for different search terms (search terms will be genre tags) at different 
times of the day, then load the genre tag in along with the video stats, no need for playlist title
or ID
'''

""" for i in genres:
    response = search(youtube, i, 5, "playlist")
    ids = getPlaylistIDFromSearch(response)
    stats = getVidStats(getPlaylistVids(ids))
    logVidData(stats, "metrics.csv", i) """

response = search(youtube, genres[0], 2, "playlist")
print(response)
print("----------------------")
ids = getPlaylistIDFromSearch(response)
print(ids)
print("----------------------")
vids = getPlaylistVids(ids)
print(vids)
print("----------------------")
stats = getVidStats(vids)
print(stats)
print("----------------------")
logVidData(stats, "metrics.csv", genres[0])
