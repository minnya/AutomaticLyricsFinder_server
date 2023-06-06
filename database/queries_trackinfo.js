
class Queries_trackinfo{

    constructor(database) {
        this.database=database;
    }

    //trackInfoの情報を取得する(artist,title)
    async getTrackInfo(artist, title) {
        let strSQL = `SELECT * FROM TrackInfo `;
        strSQL+=`WHERE artist_name = ? `;
        strSQL+=`AND track_name = ? `;
        return this.database.doQuery(strSQL, [artist, title]);
    }

    //trackInfoの情報を取得する(id)
    async getTrackInfoById(track_info_id) {
        let strSQL = `SELECT * FROM TrackInfo `;
        strSQL+=`WHERE id = ? `;
        return this.database.doQuery(strSQL, [track_info_id]);
    }

    //APIから取得したTrackInfoの情報を挿入する
    async insertTrackInfo(trackInfo){
        let strSQL = `INSERT INTO TrackInfo (artist_name, track_name, song_url, image_url,lyrics) `;
        strSQL+=`SELECT * FROM (`;
        strSQL+=`SELECT ?, ?, ?, ?, ?) AS tmp `;
        strSQL+=`WHERE NOT EXISTS `;
        strSQL+=`(SELECT * FROM TrackInfo `;
        strSQL+=`WHERE artist_name = ? `;
        strSQL+=`AND track_name = ? )`;
        return this.database.doQuery(strSQL, [trackInfo.artist, trackInfo.title, trackInfo.songUrl, trackInfo.imageUrl, trackInfo.lyrics, trackInfo.artist, trackInfo.title]);
    }
}

module.exports = Queries_trackinfo;