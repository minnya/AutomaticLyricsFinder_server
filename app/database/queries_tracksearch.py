from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
from database.manager import ScopedSession, handle_db_exceptions
from models.track_search import TrackSearch  # TrackSearch モデルが必要
from sqlalchemy.exc import IntegrityError


class QueriesTrackSearch:
    def __init__(self):
        self.session: Session = ScopedSession()

    def __del__(self):
        self.session.close()

    # TrackSearchの情報を取得する
    @handle_db_exceptions
    def get_track_search(self, artist, track, keyword):

        query = select(TrackSearch).filter(
            TrackSearch.artist_name == artist,
            TrackSearch.track_name == track,
            TrackSearch.search_keyword == keyword,
        )
        result = self.session.execute(query)
        return result.scalars().first()  # 最初の結果を返す

    # artistとtrackが一致するものが存在しない場合のみ挿入する
    @handle_db_exceptions
    def insert_track_search(self, artist, track, keyword, track_info_id):
        query = select(TrackSearch).filter(
            TrackSearch.artist_name == artist, TrackSearch.track_name == track
        )
        result = self.session.execute(query)
        existing_entry = result.scalars().first()

        if not existing_entry:
            new_entry = TrackSearch(
                artist_name=artist,
                track_name=track,
                search_keyword=keyword,
                track_info_id=track_info_id,
            )
            self.session.add(new_entry)
            self.session.commit()
            return new_entry  # 挿入したレコードを返す
        return None  # 既存レコードがある場合は挿入しない

    # artistとtrackが一致するものが存在する場合のみ更新する
    @handle_db_exceptions
    def update_track_search(self, artist, track, keyword, track_info_id):
        query = select(TrackSearch).filter(
            TrackSearch.artist_name == artist,
            TrackSearch.track_name == track,
            TrackSearch.search_keyword != keyword,
        )
        result = self.session.execute(query)
        existing_entry = result.scalars().first()

        if existing_entry:
            existing_entry.search_keyword = keyword
            existing_entry.track_info_id = track_info_id
            self.session.commit()
            return existing_entry  # 更新したレコードを返す
        return None  # 一致するレコードがなければ更新しない
