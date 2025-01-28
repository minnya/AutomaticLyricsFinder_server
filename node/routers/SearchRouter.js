const express = require('express');
const router = express.Router();

const SearchSongs = require('../controllers/searchSongs');
const KeywordProvider = require('../utils/KeywordProvider');

router.get('/', async (req, res) => {
  try {
    const artist = req.query.artist || '';
    const title = req.query.title || '';
    const keyword=KeywordProvider.getKeyword(artist,title);
    const connection = req.app.locals.connection;

    //Genius API
    const searchSongs=new SearchSongs();
    songInfoList= await searchSongs.getSongListFromApi(keyword);

    if (songInfoList.length === 0) {
        return res.status(404).json({ error: 'No songs found.' });
      }
      
    return res.json(songInfoList);
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: 'Internal server error.' });
  }
});

module.exports = router;
