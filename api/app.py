import requests
from api.config import Config as conf


def format_query(query):
    """Replaces spaces for %20"""
    return "%20".join(query.split())


def perform_response(url):
    """Perform HTTP GET REQUEST"""
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + conf.ACCESS_TOKEN,
    }
    return requests.get(url, headers=headers)


def get_artist_id(query):
    """Extract Artist Id from search results for a particular artist"""
    url = "{}search?q={}".format(conf.BASE_URL, format_query(query))
    response = perform_response(url)
    return response.json()


ids = [get_artist_id(artist_name) for artist_name in conf.ARTIST_TO_SEARCH]
