const evenNum = () => {
  console.log("The number is even!");
};

const oddNum = () => {
  console.log("The number is odd!");
};

const checkNum = (num, evenNumFunction, oddNumFunction) => {
  if (num % 2 === 0) {
    evenNumFunction();
  } else {
    oddNumFunction();
  }
};

checkNum(6, evenNum, oddNum);
