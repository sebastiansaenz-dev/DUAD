const sentence = "this is a string example";

let devidedSentence = [];

let word = "";

for (const char of sentence) {
  if (char === " ") {
    if (word.length > 0) {
      devidedSentence.push(word);
      word = "";
    }
  } else {
    word += char;
  }
}

if (word.length > 0) {
  devidedSentence.push(word);
}

console.log(devidedSentence);
