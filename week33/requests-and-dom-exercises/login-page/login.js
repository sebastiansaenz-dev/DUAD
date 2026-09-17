const loginForm = document.getElementById("login-form");

const getUser = async (userId, userPassword) => {
  try {
    const url = `https://api.restful-api.dev/objects/${userId}`;

    const response = await axios.get(url);

    return response.data;
  } catch (error) {
    return null;
    throw error;
  }
};

const logInUser = async () => {
  const loginForm = document.getElementById("login-form");
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(loginForm);
    const rawData = Object.fromEntries(formData.entries());

    const { id, password } = rawData;

    try {
      const user = await getUser(id, password);

      if (!user) {
        alert("user doesnt exists");
        throw Error("user doesnt exists");
      }

      if (user.data?.password !== password) {
        alert("incorrect password");
        throw Error("incorrect password");
      }

      alert("successfully logged in!");

      const dataToSave = {
        id: user.id,
        name: user.name,
        data: {
          email: user.data.email,
          password: user.data.password,
        },
      };
      localStorage.setItem("user", JSON.stringify(dataToSave));
      window.location.href = "../profile-page/profile.html";
    } catch (error) {
      console.error(error);
    }
  });
};

const init = () => {
  logInUser();
};

init();
