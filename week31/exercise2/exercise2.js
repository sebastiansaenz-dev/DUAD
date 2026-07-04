const fs = require("fs");

const firstFile = fs.readFile("first.txt", "utf8", (err, data1) => {
  firstFileData = data1.split("\r\n");

  fs.readFile("second.txt", "utf8", (err, data2) => {
    secondFileData = data2.split("\r\n");

    repeatedWords = [];

    for (const word of secondFileData) {
      if (firstFileData.includes(word)) {
        repeatedWords.push(word);
      }
    }
    console.log(repeatedWords.join(" "));
  });
});
