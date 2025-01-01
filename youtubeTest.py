import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from os import getenv

apiServiceName = "youtube"
version = "v3"
load_dotenv()
apiKey = getenv("ytAPIkey")

youtube = build(apiServiceName, version, developerKey=apiKey)

request = youtube.videoCategories().list(part = "snippet", regionCode = 'US')
response = request.execute()
verboseCategories = response["items"]

for i in enumerate(verboseCategories):
    print(f"Category {i[1]['id']}. {i[1]['snippet']['title']}")

#search by keyword
def search(youtube, keyword = str, maxResults = int):
    request = youtube.search().list(part = "snippet", maxResults = maxResults, q = keyword)
    return request.execute()

def getVidInfofromSearchResults(searchResults):
    vidInfo = []
    # add video id and title to list of dicts
    for i in enumerate(searchResults["items"]):
        tempdict = {"id": i[1]['id']['videoId'], "Title": i[1]['snippet']['title']}
        vidInfo.append(tempdict)
    return vidInfo

response = search(youtube, "accordion", 2)
info = getVidInfofromSearchResults(response)
print(info)