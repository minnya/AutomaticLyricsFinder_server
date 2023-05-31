const axios = require('axios');
require('dotenv').config();

const apiUrl = process.env.GENIUS_API_BASE_URL + '/search';

const headers = {
    'Authorization': `Bearer  ${process.env.GENIUS_ACCESS_TOKEN}`
  };

async function searchSongs(keyword) {

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

module.exports = searchSongs;
