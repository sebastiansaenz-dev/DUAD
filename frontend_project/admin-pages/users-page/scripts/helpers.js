export const getEl = (id) => document.getElementById(id);

export const escapeHtml = (text) => {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
};

export const capitalize = (text) =>
  text.charAt(0).toUpperCase() + text.slice(1);

export const getPrimaryRole = (user) => {
  return user.roles && user.roles.length > 0 ? user.roles[0].name : null;
};

let toastTimeoutId = null;

export const showToast = (message) => {
  const toast = getEl("toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimeoutId);
  toastTimeoutId = setTimeout(() => toast.classList.remove("show"), 2200);
};
