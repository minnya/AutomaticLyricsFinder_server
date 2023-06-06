const Database = require('./database');
const Queries_tracksearch = require('./queries_tracksearch');
const Queries_trackinfo = require('./queries_trackinfo');


class DatabaseController {

    //コンストラクタ
    constructor() {
        const database=new Database();
        this.queries_tracksearch=new Queries_tracksearch(database);
        this.queries_trackinfo=new Queries_trackinfo(database);
    }

    //すでに歌詞がデータベースにあれば返す
    async getLyrics(artist, title,keyword){
        //まずは、TrackSearchテーブルを検索する
        const searchResult=await this.queries_tracksearch.getracksearch(artist, title, keyword);
        if(searchResult==null){
            return null;
        }

        //次にTrackInfoテーブルを検索する
        const trackResult=await this.queries_trackinfo.getTrackInfoById(searchResult.track_info_id);
        if(trackResult==null){
            return null;
        }

        //戻り値を返す
        return {
            artist: trackResult.artist_name,
            title: trackResult.track_name,
            imageUrl: trackResult.image_url,
            keyword: searchResult.search_keyword,
            songUrl: trackResult.song_url,
            lyrics: trackResult.lyrics
          };
    }

    // 曲の情報を更新する
    async updateTrackDatabase(artist, title, songInfo){

        //APIの情報をTrackInfoテーブルに挿入する
        await this.queries_trackinfo.insertTrackInfo(songInfo);

        //track_info_idを取得する
        const insertedTrackInfo = await this.queries_trackinfo.getTrackInfo(songInfo.artist, songInfo.title);
        const track_info_id=insertedTrackInfo.id;

        // 次にTrackSearchテーブルを更新する (まだartist, titleがない場合)
        await this.queries_tracksearch.insertTrackSearch(artist, title, songInfo.keyword, track_info_id);

        //次にTrackSearchテーブルを更新する (すでにartist, titleがある場合)
        await this.queries_tracksearch.updateTrackSearch(artist, title, songInfo.keyword, track_info_id);
    }
  
}

module.exports = DatabaseController;
