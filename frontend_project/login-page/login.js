import { activePage } from "../utils/utils.js";
import { showErrorMessage } from "../utils/utils.js";
import { checkEmail, checkPassword } from "../utils/utils.js";

const logInUser = async (e) => {
  e.preventDefault();
  try {
    const url = "http://localhost:5002/users/login";

    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!checkEmail(email)) return;
    if (!checkPassword(password)) return;

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
