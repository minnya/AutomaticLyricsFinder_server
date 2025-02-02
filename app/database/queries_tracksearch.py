from sqlalchemy import select, insert, update
from sqlalchemy.orm import sessionmaker
from models.track_search import TrackSearch  # TrackSearch モデルが必要
from database.manager import session
from sqlalchemy.exc import IntegrityError


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
        try:
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

        except IntegrityError as e:
            # 重複エラーの場合はスルー
            if 'Duplicate entry' in str(e):
                return None
            else:
                raise

    # artistとtrackが一致するものが存在する場合のみ更新する
    def update_track_search(self, artist, track, keyword, track_info_id):
        try:
            query = select(TrackSearch).filter(
                TrackSearch.artist_name == artist,
                TrackSearch.track_name == track,
                TrackSearch.search_keyword != keyword,
            )
            result = session.execute(query)
            existing_entry = result.scalars().first()

            if existing_entry:
                existing_entry.search_keyword = keyword
                existing_entry.track_info_id = track_info_id
                session.commit()
                return existing_entry  # 更新したレコードを返す
            return None  # 一致するレコードがなければ更新しない

        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                return None
            else:
                raise  # 他のエラーは再度発生させる

