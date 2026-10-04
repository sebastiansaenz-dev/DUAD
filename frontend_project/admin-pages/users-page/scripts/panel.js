import { getEl, escapeHtml, capitalize, getPrimaryRole } from "./helpers.js";
import { findUserById, setEditingUserId, ROLE_OPTIONS } from "./state.js";

export const openEditPanel = (userId) => {
  const user = findUserById(userId);
  if (!user) return;

  setEditingUserId(userId);
  fillFormWithUser(user);
  openPanel();
};

const fillFormWithUser = (user) => {
  getEl("f_username").value = user.username;
  getEl("f_email").value = user.email;
  renderRoleSelect(getPrimaryRole(user));
};

const renderRoleSelect = (currentRole) => {
  const select = getEl("f_role");
  const options =
    currentRole && !ROLE_OPTIONS.includes(currentRole)
      ? [currentRole, ...ROLE_OPTIONS]
      : ROLE_OPTIONS;

  select.innerHTML = options
    .map(
      (role) =>
        '<option value="' +
        escapeHtml(role) +
        '">' +
        escapeHtml(capitalize(role)) +
        "</option>",
    )
    .join("");
  select.value = currentRole || ROLE_OPTIONS[0];
};

export const openPanel = () => {
  getEl("overlay").classList.add("open");
  getEl("panel").classList.add("open");
  setTimeout(() => getEl("f_username").focus(), 300);
};

export const closePanel = () => {
  getEl("overlay").classList.remove("open");
  getEl("panel").classList.remove("open");
  setEditingUserId(null);
};
