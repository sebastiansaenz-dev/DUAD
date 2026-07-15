const userId = 2;
const API_KEY = "your api key here";

const getData = async (id) => {
  const response = await fetch(`https://reqres.in/api/users/${id}`, {
    headers: {
      "x-api-key": API_KEY,
    },
  });
  return response.json();
};

const user = await getData(userId);

console.log(user);
