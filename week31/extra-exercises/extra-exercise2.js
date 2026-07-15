const names1 = ["Sebas", "Santi", "Fabi"];
const names2 = ["Ariel", "Sebas", "Fernando"];

const sameNames = (array1, array2) => {
  names = [];
  for (const name of array1) {
    if (array2.includes(name)) {
      names.push(name);
    }
  }
  console.log(names);
};

const getNames = (array1, array2, sameNamesFunction) => {
  sameNames(array1, array2);
};

getNames(names1, names2);
