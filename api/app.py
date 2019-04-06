import requests
import re
import pandas as pd


class Config:
    ACCESS_TOKEN = ""
    ARTIST_TO_SEARCH = [
        "yg",
        "nipsey hussle",
        "kendrick lamar",
        "snoop dogg",
        "2pac",
    ]
    BASE_URL = "https://api.genius.com/"


def format_query(query):
    """Replaces spaces for %20"""
    return "%20".join(query.split())


def perform_response(url):
    """Perform HTTP GET REQUEST"""
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + Config.ACCESS_TOKEN,
    }
    return requests.get(url, headers=headers)


def possible_artist_id(primary_artists):
    """Get the artist id that shows up more often"""
    if len(primary_artists) == 0:
        return None
    counts = {}
    max_id = primary_artists[0]["id"]
    counts[max_id] = 1
    for primary_artist in primary_artists:
        artist_id = primary_artist["id"]
        if artist_id not in counts:
            counts[artist_id] = 1
        counts[artist_id] += 1
        if counts[artist_id] > counts[max_id]:
            max_id = artist_id
    return max_id


def get_artist_id(query):
    """Extract artist id from search results for a particular artist"""
    url = "{}search?q={}".format(Config.BASE_URL, format_query(query))
    response = perform_response(url).json()
    check_status_code(response)
    try:
        primary_artists = [
            hit["result"]["primary_artist"]
            for hit in response["response"]["hits"]
        ]
    except KeyError:
        raise Exception("Not able to find {}".format(query))
    return possible_artist_id(primary_artists)


def check_status_code(response):
    try:
        if response["meta"]["status"] not in (202, 200):
            raise RuntimeError("Invalid access token")
    except KeyError:
        raise RuntimeError("Invalid access token")


def get_artist_songs(artist_id):
    url = "{}artists/{}/songs".format(Config.BASE_URL, artist_id)
    response = perform_response(url).json()
    check_status_code(response)
    try:
        songs = [
            get_songs_detail(song)
            for song in response["response"]["songs"]
        ]
    except KeyError:
        raise Exception("No songs exists for {}".format(artist_id))
    return songs


def get_songs_detail(song):
    artist_name = song["primary_artist"]["name"].lower()
    song_url = song["url"]
    title = remove_break_characters(song["full_title"])
    return [artist_name, song_url, title]


def remove_break_characters(sentence):
    return re.sub(r"\xa0", " ", sentence)


def main():
    contents = []
    for index, artist_name in enumerate(Config.ARTIST_TO_SEARCH):
        artist_id = get_artist_id(artist_name)
        artist_to_search = Config.ARTIST_TO_SEARCH[index].lower()
        for song in get_artist_songs(artist_id):
            if song[0] != artist_to_search:
                continue
            contents.append(song)
    dataframe = pd.DataFrame(
        contents, columns=["artist", "lyric_url", "title"]
    )
    dataframe.to_csv("lyrics_urls.csv", sep="\t")


if __name__ == "__main__":
    main()
