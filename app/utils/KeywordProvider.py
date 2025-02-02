def get_keyword(artist: str, title: str) -> str:
    keyword = ""
    for word in [artist, title]:
        word = word.lower()
        start_index = word.find("feat")
        word = word[:start_index] if start_index != -1 else word
        keyword += " " + word
    return keyword.strip()
