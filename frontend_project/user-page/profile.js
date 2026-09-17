import { showUserType, activePage } from "../utils/utils.js";

const els = {
  displayName: document.getElementById("displayName"),
  username: document.getElementById("usernameValue"),
  email: document.getElementById("emailValue"),
};

const deleteBtn = document.getElementById("deleteAccountBtn");
const toast = document.getElementById("toast");

const showToast = (message) => {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => toast.classList.remove("show"), 2200);
};

const renderUser = (user) => {
  els.displayName.textContent = `Hi, ${user.username}`;
  els.username.textContent = user.username;
  els.email.textContent = user.email;
};

const loadUser = async () => {
  try {
    const user = localStorage.getItem("user");
    const userData = JSON.parse(user);

    renderUser(userData.user);
  } catch (error) {
    console.error(error);
    showToast("Could not load your account data.");
  }
};

loadUser();

const init = () => {
  showUserType();
  activePage();
};

init();
