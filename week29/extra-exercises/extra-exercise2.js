const repeatedNums = [1, 2, 3, 2, 4, 1, 5, 2, 2, 2, 2];

let finalResult = [];

const filterNums = repeatedNums.filter((num) => {
  if (!finalResult.includes(num)) {
    finalResult.push(num);
  }
});

console.log(finalResult);
