
const searchSongs = require('./controllers_genius/searchSongs');
const getLyrics = require('./controllers_genius/getLyrics');
const express = require('express');
require('dotenv').config();
const https = require('https');
const fs = require('fs');

const options = {
    key: fs.readFileSync('/etc/letsencrypt/live/tech-blog.mydns.jp/privkey.pem', 'utf8'),
    cert: fs.readFileSync('/etc/letsencrypt/live/tech-blog.mydns.jp/cert.pem', 'utf8'),
    ca: fs.readFileSync('/etc/letsencrypt/live/tech-blog.mydns.jp/chain.pem', 'utf8')
  };

const app = express();
const port = process.env.PORT || 3000;

  
app.get('/search-lyrics', async (req, res) => {
    try {
      const keyword = req.query.keyword || '';
      const songs = await searchSongs(keyword);
      
      if (songs.length === 0) {
        return res.status(404).json({ error: 'No songs found.' });
      }
      
      const lyrics = await getLyrics(songs[0]);
      
      if (!lyrics) {
        return res.status(404).json({ error: 'Lyrics not found.' });
      }
      
      const songInfo = {
        artist: songs[0].artist,
        title: songs[0].title,
        imageUrl: songs[0].imageUrl,
        lyrics: lyrics
      };
      
      return res.json(songInfo);
    } catch (error) {
      console.error(error);
      return res.status(500).json({ error: 'Internal server error.' });
    }
  });
  
  https.createServer(options, app).listen(port, () => {
    console.log(`API server is running on port ${port}`);
  });

