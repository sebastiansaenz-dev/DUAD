const repeatedNums = [1, 2, 3, 2, 4, 1, 5, 2, 2, 2, 2];

const finalNums = (numsList) => {
  let finalResult = [];

  const filterNums = numsList.filter((num) => {
    if (!finalResult.includes(num)) {
      finalResult.push(num);
    }
  });
  return finalResult;
};

console.log(finalNums(repeatedNums));
