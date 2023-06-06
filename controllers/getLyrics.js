const axios = require('axios');
const cheerio = require('cheerio');
const Database=require('../database/database');

async function getLyrics(songInfo) {

  try{
    const songUrl = songInfo.songUrl;
    const response = await axios.get(songUrl);
    const $ = cheerio.load(response.data);

    const lyricsContainer = $('[data-lyrics-container="true"]');

    // Replace <br> with newline
    $("br", lyricsContainer).replaceWith("\n");

    // Replace the elements with their text contents
    $("a", lyricsContainer).replaceWith((_i, el) => $(el).text());

    // Remove all child elements, leaving only top-level text content
    lyricsContainer.children().remove();

    const lyrics=lyricsContainer.text();
    
    return lyrics;
  } catch (error) {
      console.error(error);
  }
}   

module.exports = getLyrics;
