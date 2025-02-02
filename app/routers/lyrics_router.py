from fastapi import APIRouter, Query, HTTPException

# 必要なインポート
from models.track_info import TrackInfo
from database.database_controller import DatabaseController
from controllers.html_parser import get_lyrics_from_html
from controllers.genius_api import search_song_genius_api
from utils.KeywordProvider import get_keyword


router = APIRouter()


@router.get("")
def get_lyrics(
    artist: str = Query("", alias="artist"),
    title: str = Query("", alias="title"),
):
    # キーワードを取得
    keyword = get_keyword(artist, title)

    # データベースから歌詞を取得
    database_controller = DatabaseController()
    result_from_db = database_controller.get_lyrics(artist, title, keyword)
    if result_from_db:
        print("データベースから歌詞を取得")
        return result_from_db

    # データベースにない場合はキーワードを基にAPIから曲情報を取得
    track_info: TrackInfo = search_song_genius_api(keyword)

    if not track_info:
        raise HTTPException(status_code=404, detail="No songs found.")

    # 曲情報内のurlから歌詞を取得
    track_info.lyrics = get_lyrics_from_html(track_info.song_url)

    # データベースを更新
    track_info=database_controller.update_track_info(track_info)
    database_controller.update_track_search(track_info.to_track_search(track_info_id=track_info.id,search_keyword=keyword, artist_name=artist, track_name=title))

    if not track_info.lyrics:
        raise HTTPException(
            status_code=404,
            detail="Lyrics not found.",
            headers={"X-SongInfo": track_info},
        )

    print("APIから歌詞を取得")
    return {
      "artist": track_info.artist_name,
      "title": track_info.track_name,
      "imageUrl": track_info.image_url,
      "songUrl": track_info.song_url,
      "keyword": keyword,
      "lyrics": track_info.lyrics
    }