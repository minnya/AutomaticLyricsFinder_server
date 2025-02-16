from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse

# 必要なインポート
from models.track_search import TrackSearch
from models.track_info import TrackInfo
from database.database_controller import DatabaseController
from controllers.html_parser import get_lyrics_from_html
from controllers.genius_api import search_song_genius_api
from utils.KeywordProvider import get_keyword


router = APIRouter()


@router.get("")
def search_lyrics(
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
        # 文字化けしないようにmedia_typeを設定する
        return JSONResponse(
            content=result_from_db, media_type="application/json; charset=utf-8"
        )

    # データベースにない場合はキーワードを基にAPIから曲情報を取得
    track_info: TrackInfo = search_song_genius_api(keyword)

    if not track_info:
        raise HTTPException(status_code=404, detail="No songs found.")

    # 曲情報内のurlから歌詞を取得
    track_info.lyrics = get_lyrics_from_html(track_info.song_url)

    # データベースを更新
    track_info = database_controller.insert_track_info(track_info)
    if not track_info:
        raise HTTPException(status_code=404, detail="No songs found.")
    track_search: TrackSearch = track_info.to_track_search(
        search_keyword=keyword, artist_name=artist, track_name=title
    )
    database_controller.update_track_search(track_search)

    if not track_info.lyrics:
        raise HTTPException(
            status_code=404,
            detail="Lyrics not found.",
            headers={"X-SongInfo": track_info},
        )

    print("APIから歌詞を取得")
    response = {
        "id": track_info.id,
        "artist": track_info.artist_name,
        "title": track_info.track_name,
        "imageUrl": track_info.image_url,
        "songUrl": track_info.song_url,
        "keyword": keyword,
        "lyrics": track_info.lyrics,
    }
    # 文字化けしないようにmedia_typeを設定する
    return JSONResponse(content=response, media_type="application/json; charset=utf-8")


@router.get("/url")
def get_lyrics_song_url(
    id: int= Query(..., description="TrackInfo ID"),
    artist: str = Query("", description="Artist Name"),
    title: str = Query("", description="Title"),
    image_url: str = Query("", description="Image Url"),
    song_url: str = Query("", description="Song Url"),
):
    # 曲情報内のurlから歌詞を取得
    lyrics = get_lyrics_from_html(song_url)

    if not lyrics:
        raise HTTPException(status_code=404, detail="Lyrics not found.")

    # データベース処理
    database_controller = DatabaseController()

    # TrackInfo の作成・更新
    track_info = TrackInfo(
        id=id,
        artist_name=artist,
        track_name=title,
        image_url=image_url,
        song_url=song_url,
        lyrics=lyrics,
        # 必要な他のフィールドを追加
    )
    track_info = database_controller.update_track_info(track_info)
    
    if not track_info:
        raise HTTPException(status_code=404, detail="Failed to update track info.")

    # レスポンス
    response = {
        "id": track_info.id,
        "artist": track_info.artist_name,
        "title": track_info.track_name,
        "imageUrl": track_info.image_url,
        "lyrics": track_info.lyrics,
    }

    # 文字化けしないようにmedia_typeを設定する
    return JSONResponse(content=response, media_type="application/json; charset=utf-8")
