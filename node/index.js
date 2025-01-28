const express = require('express');
require('dotenv').config();
const http = require('http');  // httpsからhttpに変更
const fs = require('fs');

const LyricsRouter = require('./routers/LyricsRouter');
const SeatchRouter = require('./routers/SearchRouter');
const Database = require('./database/database');

const app = express();
const port = process.env.PORT || 3000;

app.locals.connection = new Database().getConnection();

// config
app.timeout = 10000;

// routes
app.use('/search-lyrics', LyricsRouter);
app.use('/search-songs', SeatchRouter);

// https.createServer(options, app).listen(port, () => {
//   console.log(`API server is running on port ${port}`);
// });

http.createServer(app).listen(port, () => {  // httpでリスンするよう変更
  console.log(`API server is running on port ${port}`);
});
