const postData = async (data) => {
  const url = "https://api.restful-api.dev/objects";

  try {
    const response = await axios.post(url, data);

    console.log("user created!");
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(`Error in the request: ${error}`);
    throw error;
  }
};

const sendData = () => {
  const registerForm = document.getElementById("register-form");
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(registerForm);
    const rawData = Object.fromEntries(formData.entries());

    const { name, password, ...otherFields } = rawData;

    const userData = {
      name: name,
      data: {
        ...otherFields,
        password: password,
      },
    };

    try {
      const responseData = await postData(userData);

      const userId = responseData.id;

      alert(`User successfully created! Your id is: ${userId}`);

      const dataToSave = {
        id: responseData.id,
        name: responseData.name,
        data: {
          ...otherFields,
          password: password,
        },
      };

      localStorage.setItem("user", JSON.stringify(dataToSave));

      window.location.href = "../profile-page/profile.html";
    } catch (error) {
      console.error(error);
      alert("there was an error creating the user");
    }
  });
};

const init = () => {
  sendData();
};

init();
