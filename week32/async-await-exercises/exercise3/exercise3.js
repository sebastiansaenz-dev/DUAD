const userId = 2;
const API_KEY = "your api key here";

const divResult = document.getElementById("result");
const input = document.getElementById("user-id");
const button = document.getElementById("send-user-id-button");

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

const showData = async () => {
  try {
    const UserId = input.value;
    const userData = await getData(UserId);

    if (!userData) {
      throw Error("user not found");
    }

    divResult.innerHTML = "";

    const userFirstName = document.createElement("h2");
    const userLastName = document.createElement("h2");
    const userEmail = document.createElement("h2");

    userFirstName.innerHTML = userData.data.first_name;
    userLastName.innerHTML = userData.data.last_name;
    userEmail.innerHTML = userData.data.email;

    divResult.appendChild(userFirstName);
    divResult.appendChild(userLastName);
    divResult.appendChild(userEmail);

    input.value = "";
  } catch (error) {
    divResult.innerHTML = "";
    const errorElement = document.createElement("h2");
    errorElement.innerHTML = error.message;
    divResult.appendChild(errorElement);
  }
};

button.addEventListener("click", showData);
