const words = ["very", "dogs", "cute", "are"];

const createPromises = (word, delay) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(word);
    }, delay);
  });
};

const promises = [
  createPromises(words[1], 1000),
  createPromises(words[3], 2000),
  createPromises(words[0], 3000),
  createPromises(words[2], 4000),
];

Promise.all(promises).then((result) => {
  console.log(result.join(" "));
});
