import { activePage, apiPublic } from "../utils/utils.js";
import { showErrorMessage } from "../utils/utils.js";
import { checkEmail, checkPassword } from "../utils/utils.js";

const createUser = async (e) => {
  e.preventDefault();
  try {
    const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    const username = usernameInput.value;
    const email = emailInput.value;
    const password = passwordInput.value;

    if (!checkEmail(email)) return;
    if (!checkPassword(password)) return;

    const userData = {
      username: username,
      email: email,
      password: password,
    };

    const response = await apiPublic.post("/users/register-user", userData);

    localStorage.setItem("user", JSON.stringify(response.data));

    window.location.href = "../product-catalog-page/products.html";
  } catch (error) {
    showErrorMessage(error);
  }
};

const init = () => {
  activePage();

  const registerForm = document.getElementById("register-form");

  if (registerForm) {
    registerForm.addEventListener("submit", createUser);
  }
};

init();
