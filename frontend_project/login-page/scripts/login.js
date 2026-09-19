import {
  activePage,
  showErrorMessage,
  checkEmail,
  checkPassword,
} from "../../utils/utils.js";
import { loginRequest } from "./api.js";

const logInUser = async (e) => {
  e.preventDefault();
  try {
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!checkEmail(email)) return;
    if (!checkPassword(password)) return;

    const user = await loginRequest(email, password);

    localStorage.setItem("user", JSON.stringify(user));

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
