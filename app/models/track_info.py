from sqlalchemy import Column, Integer, String, Text
from models.track_search import TrackSearch
from database.manager import Base


class TrackInfo(Base):
    __tablename__ = "TrackInfo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String(255), nullable=False)
    track_name = Column(String(255), nullable=False)
    song_url = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    lyrics = Column(Text, nullable=True)

    def __repr__(self):
        return f"<TrackInfo(id={self.id}, artist_name={self.artist_name}, track_name={self.track_name})>"

    def to_track_search(self,search_keyword: str = "", artist_name: str="", track_name: str=""):
        """
        TrackInfo から TrackSearch を作成する
        :param search_keyword: 検索キーワード
        :return: TrackSearch オブジェクト
        """
        return TrackSearch(
            artist_name=artist_name,
            track_name=track_name,
            search_keyword=search_keyword,
            track_info_id=self.id
        )