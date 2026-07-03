const sentence = "This is a test. This test is simple";

let devidedSentence = [];

let word = "";

const wordCounter = (sentence) => {
  const sanitizeSentence = (finalSentence = sentence
    .toLowerCase()
    .replace(/[^\w\s]/g, ""));
  const words = sanitizeSentence.split(" ");
  const countWords = {};

  for (const word of words) {
    countWords[word] = (countWords[word] || 0) + 1;
  }
  return countWords;
};

console.log(wordCounter(sentence));
