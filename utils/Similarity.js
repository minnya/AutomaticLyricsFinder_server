

function getWordFrequencyMap(str) {
    const words = str.split(' ');
    const frequencyMap = {};

    words.forEach(word => {
        if (!frequencyMap[word]) {
            frequencyMap[word] = 0;
        }
        frequencyMap[word]++;
    });

    return frequencyMap;
}

function getSimilarity(str1, str2) {
    const map1 = getWordFrequencyMap(str1);
    const map2 = getWordFrequencyMap(str2);

    let commonWordCount = 0;

    for (let word in map1) {
        if (map2[word]) {
            commonWordCount += Math.min(map1[word], map2[word]);
        }
    }

    return commonWordCount / Math.max(str1.split(' ').length, str2.split(' ').length);
}

module.exports = getSimilarity;