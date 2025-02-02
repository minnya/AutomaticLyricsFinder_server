import requests
import os
from models.genius_api_model import GeniusApiModel
from models.track_info import TrackInfo
from utils.Similarity import get_similarity

# Genius APIの設定
GENIUS_API_BASE_URL = os.getenv("GENIUS_API_BASE_URL")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
API_URL = f"{GENIUS_API_BASE_URL}/search"
HEADERS = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}

# Genius APIにリクエストを送信して結果を取得（同期処理）
def _request_api(keyword: str) -> list[GeniusApiModel]:
    search_query = {"q": keyword}
    response = requests.get(API_URL, headers=HEADERS, params=search_query)

    response_data = response.json()
    hits = response_data["response"]["hits"]
    songs = [
        GeniusApiModel(
            artist_name=hit["result"]["artist_names"],
            track_name=hit["result"]["title"],
            image_url=hit["result"]["header_image_thumbnail_url"],
            song_url=hit["result"]["url"],
            keyword=keyword
        )
        for hit in hits
    ]

    return songs

def get_songs_from_genius_api(keyword: str)-> list[GeniusApiModel]:
    return _request_api(keyword)

def get_song_from_genius_api(keyword: str) -> TrackInfo:
    song_list: list[GeniusApiModel] = get_songs_from_genius_api(keyword)

    if not song_list:
        return {"message": "No songs found."}

    # 類似度が最も高い曲を見つける
    highest_similarity_song = max(song_list, key=lambda song: song.similarity)

    return highest_similarity_song.to_track_info()
