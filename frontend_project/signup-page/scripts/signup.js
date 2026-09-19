import {
  activePage,
  showErrorMessage,
  checkEmail,
  checkPassword,
} from "../../utils/utils.js";
import { registerUserRequest } from "./api.js";

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

    const user = await registerUserRequest(username, email, password);
    localStorage.setItem("user", JSON.stringify(user));

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
