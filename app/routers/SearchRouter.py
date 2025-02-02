from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from pydantic import BaseModel

# 必要なインポート
from controllers.genius_api import get_songs_from_genius_api
from utils.KeywordProvider import get_keyword

router = APIRouter()


# Pydanticモデル
class SongInfo(BaseModel):
    artist: str
    title: str
    songUrl: str
    imageUrl: str
    keyword: str


@router.get("")
def get_song_list(
    artist: str = Query("", alias="artist"), title: str = Query("", alias="title")
):
    # キーワードを取得
    keyword = get_keyword(artist, title)

    # Genius APIから曲リストを取得
    song_info_list = get_songs_from_genius_api(keyword)

    if not song_info_list:
        raise HTTPException(status_code=404, detail="No songs found.")

    return song_info_list
