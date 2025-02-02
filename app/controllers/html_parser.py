import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

def get_lyrics_from_html(song_url: str) -> str:
    # HTTPリクエスト（同期）
    response = requests.get(song_url)

    # レスポンスが正常でない場合
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to fetch the lyrics."
        )

    # BeautifulSoupを使ってHTMLをパース
    soup = BeautifulSoup(response.text, "html.parser")

    # すべての"data-lyrics-container"を持つ要素を取得
    lyrics_containers = soup.find_all(attrs={"data-lyrics-container": "true"})

    if not lyrics_containers:
        raise HTTPException(status_code=404, detail="Lyrics container not found.")

    lyrics_list = []
    
    for container in lyrics_containers:
        # <br>タグを改行に置き換え
        for br_tag in container.find_all("br"):
            br_tag.replace_with("\n")

        # <a>タグをそのテキストに置き換え
        for a_tag in container.find_all("a"):
            a_tag.replace_with(a_tag.get_text())

        # 子要素をすべて削除して、テキストだけを残す
        for child in container.findChildren():
            child.extract()

        # テキストをリストに追加
        lyrics_list.append(container.get_text(strip=False))
    
    # すべての歌詞を結合
    lyrics = "\n".join(lyrics_list)

    return lyrics
