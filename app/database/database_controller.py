from fastapi import FastAPI
from models.track_info import TrackInfo
from models.track_search import TrackSearch
from database.queries_tracksearch import QueriesTrackSearch
from database.queries_trackinfo import QueriesTrackInfo

app = FastAPI()


class DatabaseController:
    def __init__(self):
        self.queries_tracksearch = QueriesTrackSearch()
        self.queries_trackinfo = QueriesTrackInfo()

    def get_lyrics(self, artist: str, title: str, keyword: str):
        # TrackSearchテーブルを検索
        search_result = self.queries_tracksearch.get_track_search(
            artist, title, keyword
        )
        if search_result is None:
            return None

        # TrackInfoテーブルを検索
        track_result = self.queries_trackinfo.get_track_info_by_id(
            search_result.track_info_id
        )
        if track_result is None:
            return None

        # 戻り値を作成して返す
        return {
            "artist": track_result.artist_name,
            "title": track_result.track_name,
            "imageUrl": track_result.image_url,
            "keyword": search_result.search_keyword,
            "songUrl": track_result.song_url,
            "lyrics": track_result.lyrics,
        }

    def update_track_info(self, song_info: TrackInfo)->TrackInfo:
        # APIの情報をTrackInfoテーブルに挿入
        inserted_track_info= self.queries_trackinfo.insert_track_info(song_info)
        return inserted_track_info

    def update_track_search(self, search_info: TrackSearch):

        # TrackSearchテーブルを更新
        self.queries_tracksearch.insert_track_search(
            search_info.artist_name,
            search_info.track_name,
            search_info.search_keyword,
            search_info.track_info_id,
        )
        self.queries_tracksearch.update_track_search(
            search_info.artist_name,
            search_info.track_name,
            search_info.search_keyword,
            search_info.track_info_id,
        )
