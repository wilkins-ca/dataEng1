from sp_search import search

def getTop100ArtistsInGenre(genreTag = str, accessToken = str):
    resp = search(genreTag, 100, "artist", accessToken)
    if resp.status_code == 200:
        print("successful request")
        print(resp)
        artistList = []
        for i in enumerate(resp.json()['artists']['items']):
            count = 1
            name = i[1]['name'] #string
            popularity = i[1]['popularity'] #int
            genres = i[1]['genres'] #genres is a list
            print("Name: " + name)
            print("Popularity: " + str(popularity))
            print("Genres:")
            print(genres)

            artist = [name, popularity, genres]
            artistList.append(artist) #appending to artist dictionary
            count += 1
        return artistList
    else:
        print("Unsuccessful request")
        print(resp)
        return None


def getTop100ArtistsByLang(lang = str, accessToken = str):
    # change limit to 100 once testing is done
    resp = search(lang, 10, "artist", 'US', accessToken)
    if resp.status_code == 200:
        print("Successful Request")
        artistList = []
        for i in enumerate(resp.json()['artists']['items']):
            count = 1
            name = i[1]['name'] #string
            popularity = i[1]['popularity'] #int
            genres = i[1]['genres'] #genres is a list
            print("Name: " + name)
            print("Popularity: " + str(popularity))
            print("Genres:")
            print(genres)

            artist = {"Name": name, "Popularity": popularity, "Genres": genres}
            artistList.append(artist) #appending to artist dictionary
            count += 1
        return artistList
    else:
        print("Unsuccessful Request: Status Code = " + str(resp.status_code))
        print(resp.text)
        return None