import { showUserType, activePage } from "../../utils/utils.js";
import { renderUser, showToast } from "./render.js";

const loadUser = () => {
  try {
    const user = localStorage.getItem("user");
    const userData = JSON.parse(user);
    renderUser(userData.user);
  } catch (error) {
    console.error(error);
    showToast("Could not load your account data.");
  }
};

const init = () => {
  loadUser();
  showUserType();
  activePage();
};

init();
