from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup


async def get_lyrics_from_html(song_url: str) -> str:
    # HTTPリクエスト
    async with httpx.AsyncClient() as client:
        response = await client.get(song_url)

    # レスポンスが正常でない場合
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to fetch the lyrics."
        )

    # BeautifulSoupを使ってHTMLをパース
    soup = BeautifulSoup(response.text, "html.parser")

    # ルビーの部分を取得
    lyrics_container = soup.find(attrs={"data-lyrics-container": "true"})

    if not lyrics_container:
        raise HTTPException(status_code=404, detail="Lyrics container not found.")

    # <br>タグを改行に置き換え
    for br_tag in lyrics_container.find_all("br"):
        br_tag.replace_with("\n")

    # <a>タグをそのテキストに置き換え
    for a_tag in lyrics_container.find_all("a"):
        a_tag.replace_with(a_tag.get_text())

    # 子要素をすべて削除して、テキストだけを残す
    for child in lyrics_container.findChildren():
        child.extract()

    # 最終的な歌詞を取得
    lyrics = lyrics_container.get_text(strip=True)

    return lyrics
