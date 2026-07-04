const positiveNumber = (num) => {
  console.log(`Valid number: ${num}`);
};

const negativeNumber = (num) => {
  console.log(`Negative number: ${num}`);
};

const validateInput = (num, positiveFunction, negativeFunction) => {
  if (num > 0) {
    positiveFunction(num);
  } else if (num < 0) {
    negativeFunction(num);
  } else {
    console.log("num is 0");
  }
};

validateInput(0, positiveNumber, negativeNumber);
