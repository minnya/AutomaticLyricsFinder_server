from sqlalchemy.future import select
from sqlalchemy import insert, exists
from sqlalchemy.orm import Session
from database.manager import ScopedSession, handle_db_exceptions
from models.track_info import TrackInfo  # TrackInfoモデルを使用


class QueriesTrackInfo:
    def __init__(self):
        self.session: Session = ScopedSession()

    def __del__(self):
        self.session.close()

    # TrackInfoの情報を取得する(artist, title)
    @handle_db_exceptions
    def get_track_info(self, artist: str, title: str) -> TrackInfo:
        stmt = select(TrackInfo).where(
            TrackInfo.artist_name == artist, TrackInfo.track_name == title
        )
        result = self.session.execute(stmt)
        return result.scalars().first()  # モデルインスタンスのリストを返す

    # TrackInfoの情報を取得する(id)
    @handle_db_exceptions
    def get_track_info_by_id(self, track_info_id: int):
        stmt = select(TrackInfo).where(TrackInfo.id == track_info_id)
        result = self.session.execute(stmt)
        return result.scalars().first()  # 1件の結果を返す

    # APIから取得したTrackInfoの情報を挿入する
    @handle_db_exceptions
    def insert_track_info(self, track_info: TrackInfo) -> TrackInfo:
        trackinfos = (
            self.session.query(TrackInfo)
            .where(
                TrackInfo.artist_name == track_info.artist_name,
                TrackInfo.track_name == track_info.track_name,
            )
            .all()
        )

        exists_result = bool(trackinfos)

        if not exists_result:  # データが存在しない場合に挿入
            new_track_info = TrackInfo(
                artist_name=track_info.artist_name,
                track_name=track_info.track_name,
                song_url=track_info.song_url,
                image_url=track_info.image_url,
                lyrics=track_info.lyrics or "",  # lyricsがNoneの場合は空文字列
            )
            self.session.add(new_track_info)
            self.session.commit()  # 挿入を確定

        return self.get_track_info(track_info.artist_name, track_info.track_name)
