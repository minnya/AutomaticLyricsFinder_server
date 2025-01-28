class KeywordProvider{
    
    //検索用キーワードを作成
    static getKeyword(artist,titile){
        let keyword="";
        for(let word of [artist,titile]){
        word = word.toLowerCase();
        const startIndex = word.indexOf("feat");
        word = startIndex !== -1 ? word.substring(0, startIndex) : word;
        keyword += " " +word;
        }
        return keyword.trim();
    }
}

module.exports = KeywordProvider;