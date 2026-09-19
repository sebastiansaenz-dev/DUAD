const els = {
  displayName: document.getElementById("displayName"),
  username: document.getElementById("usernameValue"),
  email: document.getElementById("emailValue"),
};

const toast = document.getElementById("toast");

export const showToast = (message) => {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => toast.classList.remove("show"), 2200);
};

export const renderUser = (user) => {
  els.displayName.textContent = `Hi, ${user.username}`;
  els.username.textContent = user.username;
  els.email.textContent = user.email;
};
