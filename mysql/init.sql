-- TrackInfoテーブルの作成
CREATE TABLE TrackInfo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    track_name VARCHAR(255) NOT NULL,
    song_url VARCHAR(255),
    image_url VARCHAR(255),
    lyrics TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    UNIQUE (artist_name, track_name)
);

-- TrackSearchテーブルの作成
CREATE TABLE TrackSearch (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    track_name VARCHAR(255) NOT NULL,
    search_keyword VARCHAR(255) NOT NULL,
    track_info_id INT,
    FOREIGN KEY (track_info_id) REFERENCES TrackInfo(id),
    UNIQUE (artist_name, track_name, search_keyword)
);