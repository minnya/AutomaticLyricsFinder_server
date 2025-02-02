from sqlalchemy import select, insert, update
from sqlalchemy.orm import sessionmaker
from models.track_search import TrackSearch  # TrackSearch モデルが必要
from database.manager import session


class QueriesTrackSearch:
    # TrackSearchの情報を取得する
    def get_track_search(self, artist, track, keyword):
        query = select(TrackSearch).filter(
            TrackSearch.artist_name == artist,
            TrackSearch.track_name == track,
            TrackSearch.search_keyword == keyword,
        )
        result = session.execute(query)
        return result.scalars().first()  # 最初の結果を返す

    # artistとtrackが一致するものが存在しない場合のみ挿入する
    def insert_track_search(self, artist, track, keyword, track_info_id):
        query = select(TrackSearch).filter(
            TrackSearch.artist_name == artist, TrackSearch.track_name == track
        )
        result = session.execute(query)
        existing_entry = result.scalars().first()

        if not existing_entry:
            new_entry = TrackSearch(
                artist_name=artist,
                track_name=track,
                search_keyword=keyword,
                track_info_id=track_info_id,
            )
            session.add(new_entry)
            session.commit()
            return new_entry  # 挿入したレコードを返す
        return None  # 既存レコードがある場合は挿入しない

    # artistとtrackが一致するものが存在する場合のみ更新する
    def update_track_search(self, artist, track, keyword, track_info_id):
        query = select(TrackSearch).filter(
            TrackSearch.artist_name == artist,
            TrackSearch.track_name == track,
            TrackSearch.search_keyword != keyword,
        )
        result = session.execute(query)
        existing_entry = result.scalars().first()

        if existing_entry:
            existing_entry.keyword = keyword
            existing_entry.track_info_id = track_info_id
            session.commit()
            return existing_entry  # 更新したレコードを返す
        return None  # 一致するレコードがなければ更新しない
