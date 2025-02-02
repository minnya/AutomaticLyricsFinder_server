from collections import Counter


def get_word_frequency_map(s: str) -> dict:
    words = s.lower().split(" ")
    frequency_map = Counter(words)
    return dict(frequency_map)


def get_similarity(str1: str, str2: str) -> float:
    map1 = get_word_frequency_map(str1)
    map2 = get_word_frequency_map(str2)

    common_word_count = 0

    for word in map1:
        if word in map2:
            common_word_count += min(map1[word], map2[word])

    return common_word_count / max(len(str1.split(" ")), len(str2.split(" ")))
