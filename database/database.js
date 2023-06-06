const mysql = require('mysql2/promise');
require('dotenv').config();

class Database {
  constructor() {
    this.connection = mysql.createPool({
      host: process.env.DATABASE_HOST,
      user: process.env.DATABASE_USER,
      password: process.env.DATABASE_PASSWORD,
      database: process.env.DATABASE_NAME,
    });
  }

  //クエリを実行する
  async doQuery(strSQL, params){
    try {
      console.log(strSQL);
      const [results,] = await this.connection.query(strSQL, params);
      const lastIndex = results.length - 1;
      return results[lastIndex];
    } catch (err) {
      console.error('データの取得中にエラーが発生しました: ' + err.stack);
      throw err;
    }
  }
}

module.exports = Database;
