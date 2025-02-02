from sqlalchemy import Column, Integer, String
from database.manager import Base


class TrackSearch(Base):
    __tablename__ = "TrackSearch"

    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String(255), nullable=False)
    track_name = Column(String(255), nullable=False)
    search_keyword = Column(String(255), nullable=False)
    track_info_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<TrackSearch(id={self.id}, artist_name={self.artist_name}, track_name={self.track_name}, search_keyword={self.search_keyword})>"
