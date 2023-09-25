const express = require('express');
const router = express.Router();

const getLyrics = require('../controllers/getLyrics');
const SearchSongs = require('../controllers/searchSongs');
const DatabaseController = require('../database/database_controller');
const KeywordProvider = require('../utils/KeywordProvider');

const searchSongs=new SearchSongs();

router.get('/', async (req, res) => {
  try {
    const artist = req.query.artist || '';
    const title = req.query.title || '';
    const keyword=KeywordProvider.getKeyword(artist,title);
    const connection = req.app.locals.connection;

    //データベースの情報を確認する
    const databaseController=new DatabaseController(connection);
    const resultFromDd = await databaseController.getLyrics(artist, title,keyword);
    if(resultFromDd!=null){
      console.log("データベースから歌詞を取得");
      return res.json(resultFromDd);
    }

    //データベースにない場合はAPIから取得する
    song = await searchSongs.getSong(artist,title,keyword);

    console.log(song);

    if (song==null) {
      return res.status(404).json({ error: 'No songs found.' });
  }

    const lyrics = await getLyrics(song);

    const songInfo = {
      artist: song.artist,
      title: song.title,
      imageUrl: song.imageUrl,
      songUrl: song.songUrl,
      keyword: song.keyword,
      lyrics: lyrics
    };

    //データベースを更新する
    await databaseController.updateTrackDatabase(artist, title, songInfo);

    //APIで歌詞が見つからない場合はエラーを返す
    if (!lyrics) {
      return res.status(404).json({ error: 'Lyrics not found.', data: songInfo });
    }

    console.log("APIから歌詞を取得");
    return res.json(songInfo);
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: 'Internal server error.' });
  }
});

module.exports = router;
