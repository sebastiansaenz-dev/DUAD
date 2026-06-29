const sentence = "this is a string example";

let devided_sentence = [];

let word = "";

for (const char of sentence) {
  if (char === " ") {
    if (word.length > 0) {
      devided_sentence.push(word);
      word = "";
    }
  } else {
    word += char;
  }
}

if (word.length > 0) {
  devided_sentence.push(word);
}

console.log(devided_sentence);
