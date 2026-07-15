const userId = 23;
const API_KEY = "your api key here";

const getData = async (id) => {
  try {
    const response = await fetch(`https://reqres.in/api/users/${id}`, {
      headers: {
        "x-api-key": API_KEY,
      },
    });

    if (response.status === 404) {
      throw new Error("User not found");
    }

    const data = await response.json();

    return data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

const user = await getData(userId);

if (user) {
  console.log(user);
}
