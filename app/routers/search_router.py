from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# 必要なインポート
from models.genius_api_model import GeniusApiModel
from controllers.genius_api import search_songs_genius_api
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
    song_info_list: list[GeniusApiModel] = search_songs_genius_api(keyword)

    # "Genius" を含むアーティストを除外
    song_info_list = [song for song in song_info_list if "Genius" not in song.artist_name]

    if not song_info_list:
        raise HTTPException(status_code=404, detail="No songs found.")

    response = [song_info.to_dict() for song_info in song_info_list]

    return JSONResponse(content=response, media_type="application/json; charset=utf-8")
