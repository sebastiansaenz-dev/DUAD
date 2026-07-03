const sentence = "JavaScript and Python";

const revertSentence = (sentence) => {
  let finalSentence = "";

  for (let i = sentence.length - 1; i >= 0; i--) {
    finalSentence += sentence[i];
  }

  return finalSentence;
};

console.log(revertSentence(sentence));
