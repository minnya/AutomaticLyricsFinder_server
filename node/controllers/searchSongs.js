const axios = require('axios');
require('dotenv').config();
const similarity = require('../utils/Similarity');
const DatabaseController = require('../database/database_controller');

apiUrl = process.env.GENIUS_API_BASE_URL + '/search';

headers = {
    'Authorization': `Bearer  ${process.env.GENIUS_ACCESS_TOKEN}`
  };

class SearchSongs{
  //GeniusAPI
  async #requestApi(keyword) {

      const searchQuery = {
          "q": keyword
      }
      try {
        const response = await axios.get(apiUrl, {
          headers: headers,
          params: searchQuery
        });
    
        const hits = response.data.response.hits;
        const songs = hits.map(hit => {
          const result = hit.result;
          return {
            artist: result.artist_names,
            title: result.title,
            imageUrl: result.header_image_thumbnail_url,
            songUrl: result.url
          };
        });
    
        return songs;
      } catch (error) {
        console.error(error);
      }
  } 

  

  //メイン処理APIから取得
  async getSongListFromApi(keyword){

    let songs=await this.#requestApi(keyword);

    const songInfoList = songs.map((song) => {
        return {
          artist: song.artist,
          title: song.title,
          similarity: similarity(keyword, song.title+" "+song.artist),
          imageUrl: song.imageUrl,
          keyword: keyword,
          songUrl: song.songUrl,
          lyrics: song.lyrics
        };
      });
      return songInfoList;
  }

  async getSong(artist,title,keyword){
    
    //上記がなければ、APIを試す
    const songList = await this.getSongListFromApi(keyword);

    if (songList.length === 0) {
        return null;
    }

    let highestSimilarity = -1; // 最大のsimilarity値を初期化
    let songWithHighestSimilarity = null; // 最大のsimilarity値を持つ要素を初期化

    for (const song of songList) {
        if (song.similarity > highestSimilarity) {
            highestSimilarity = song.similarity;
            songWithHighestSimilarity = song;
        }
    }
    return songWithHighestSimilarity;
  }
}

module.exports = SearchSongs;
