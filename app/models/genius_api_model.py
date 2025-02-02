# 曲の情報モデル
from models.track_info import TrackInfo
from utils.Similarity import get_similarity


class GeniusApiModel:
    def __init__(self, artist_name: str, track_name: str,
                 image_url: str, keyword: str, song_url: str, lyrics: str = None):
        self.artist_name = artist_name
        self.track_name = track_name
        self.similarity = get_similarity(
            keyword, f"{track_name} {artist_name}"
        )
        self.image_url = image_url
        self.song_url = song_url
        self.lyrics = lyrics

    def to_track_info(self) -> TrackInfo:
        return TrackInfo(
            artist_name=self.artist_name,
            track_name=self.track_name,
            song_url=self.song_url,
            image_url=self.image_url,
            lyrics=self.lyrics
        )