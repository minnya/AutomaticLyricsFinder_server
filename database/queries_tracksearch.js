
class Queries_tracksearch{
    constructor(database) {
        this.database=database;
    }

    //TrackSearchの情報を取得する
    async getracksearch(artist, track, keyword) {
        let strSQL = `SELECT * FROM TrackSearch `;
        strSQL+=`WHERE artist_name = ? `;
        strSQL+=`AND track_name = ? `;
        strSQL+=`AND search_keyword = ? `;
        return this.database.doQuery(strSQL, [artist, track, keyword]);
    }

    //artistとtrackが一致するものが存在しない場合のみ挿入する
    async insertTrackSearch(artist, track, keyword, track_info_id) {
        let strSQL = `INSERT INTO TrackSearch (artist_name, track_name, search_keyword, track_info_id) `;
        strSQL+=`SELECT * FROM (`;
        strSQL+=`SELECT ?, ?, ?, ?) AS tmp `;
        strSQL+=`WHERE NOT EXISTS `;
        strSQL+=`(SELECT * FROM TrackSearch `;
        strSQL+=`WHERE artist_name = ? `;
        strSQL+=`AND track_name = ?) `;
        return this.database.doQuery(strSQL, [artist, track, keyword, track_info_id, artist, track]);
    }

    //artistとtrackが一致するものが存在する場合のみ更新する
    async updateTrackSearch(artist, track, keyword, track_info_id) {
        let strSQL = `UPDATE TrackSearch `;
        strSQL+=`SET search_keyword = ?, `;
        strSQL+=`track_info_id = ? `;
        strSQL+=`WHERE artist_name = ? `;
        strSQL+=`AND track_name = ? `;
        strSQL+=`AND search_keyword != ? `;
        return this.database.doQuery(strSQL, [keyword, track_info_id, artist, track, keyword]);
    }
}

module.exports = Queries_tracksearch;