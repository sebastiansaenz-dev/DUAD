import { activePage } from "../utils/utils.js";
import { showErrorMessage } from "../utils/utils.js";

const logInUser = async (e) => {
  e.preventDefault();
  try {
    const url = "http://localhost:5002/users/login";

    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    const email = emailInput.value;
    const password = passwordInput.value;

    const userData = {
      email: email,
      password: password,
    };

    const response = await axios.post(url, userData);

    localStorage.setItem("user", JSON.stringify(response.data));

    window.location.href = "../product-catalog-page/products.html";
  } catch (error) {
    showErrorMessage(error);
  }
};

const init = () => {
  const loginForm = document.getElementById("login-form");

  if (loginForm) {
    loginForm.addEventListener("submit", logInUser);
  }

  activePage();
};

init();
