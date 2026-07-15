const userId = 2;
const API_KEY = "your api key here";

const response = fetch(`https://reqres.in/api/users/${userId}`, {
  headers: {
    "x-api-key": API_KEY,
  },
});

response
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.log(`there was an error ${error}`);
  });
