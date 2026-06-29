const sentence = "JavaScript and Python";

let finalWord = "";

for (let i = sentence.length - 1; i >= 0; i--) {
  finalWord += sentence[i];
  console.log(sentence[i]);
}

console.log(finalWord);
