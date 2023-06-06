
const express = require('express');
require('dotenv').config();
const https = require('https');
const fs = require('fs');

const LyricsRouter = require('./routers/LyricsRouter');
const SeatchRouter = require('./routers/SearchRouter');

const options = {
    key: fs.readFileSync('/etc/letsencrypt/live/tech-blog.mydns.jp/privkey.pem', 'utf8'),
    cert: fs.readFileSync('/etc/letsencrypt/live/tech-blog.mydns.jp/cert.pem', 'utf8'),
    ca: fs.readFileSync('/etc/letsencrypt/live/tech-blog.mydns.jp/chain.pem', 'utf8')
  };

const app = express();
const port = process.env.PORT || 3000;

//config
app.timeout = 10000;

//routes
app.use('/search-lyrics', LyricsRouter);
app.use('/search-songs', SeatchRouter);

https.createServer(options, app).listen(port, () => {
    console.log(`API server is running on port ${port}`);
});

