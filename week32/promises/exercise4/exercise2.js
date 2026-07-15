const userId = 23;
const API_KEY = "free_user_3Fyp7nwVCnbPbcEWualksRHVQvg";

const response = fetch(`https://reqres.in/api/users/${userId}`, {
  headers: {
    "x-api-key": API_KEY,
  },
});

response
  .then((result) => {
    if (result.status === 404) {
      throw Error("User not found");
    }
  })
  .catch((error) => {
    console.log(error);
  });
