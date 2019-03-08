import requests


class Config:
    ACCESS_TOKEN = ""
    ARTIST_TO_SEARCH = ["bad bunny", "yg", "nipsey hussle"]
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
    url = "{}search?q={}&offset=10&limit=5".format(
        Config.BASE_URL, format_query(query)
    )
    response = perform_response(url).json()
    primary_artists = [
        hit["result"]["primary_artist"] for hit in response["response"]["hits"]
    ]
    return possible_artist_id(primary_artists)


def main():
    ids = [
        get_artist_id(artist_name) for artist_name in Config.ARTIST_TO_SEARCH
    ]
    print(ids)


if __name__ == "__main__":
    main()
