import { getEl, showToast } from "./helpers.js";
import { updateUserRequest, deleteUserRequest } from "./api.js";
import {
  getEditingUserId,
  findUserById,
  removeUserFromState,
  applyUpdateToLocalUser,
  setSearchTerm,
  setCurrentPage,
} from "./state.js";
import { closePanel } from "./panel.js";
import { renderAll } from "./render.js";

export const handleFormSubmit = async (e) => {
  e.preventDefault();
  const editingUserId = getEditingUserId();
  if (!editingUserId) return;

  const payload = {
    username: getEl("f_username").value.trim(),
    email: getEl("f_email").value.trim(),
    roles: [getEl("f_role").value],
  };

  if (!payload.username || !payload.email) {
    showToast("Please fill in all required fields.");
    return;
  }

  const saveBtn = getEl("saveBtn");
  saveBtn.disabled = true;

  try {
    const updated = await updateUserRequest(editingUserId, payload);
    applyUpdateToLocalUser(editingUserId, updated || payload);
    closePanel();
    renderAll();
    showToast("User updated.");
  } catch (error) {
    console.error(error);
    showToast("Something went wrong while saving.");
  } finally {
    saveBtn.disabled = false;
  }
};

export const handleDeleteClick = async (id) => {
  const user = findUserById(id);
  if (!user) return;

  const confirmed = confirm('Remove "' + user.username + '" from the system?');
  if (!confirmed) return;

  try {
    await deleteUserRequest(id);
    removeUserFromState(id);
    renderAll();
    showToast("User deleted.");
  } catch (error) {
    console.error(error);
    showToast("Could not delete the user.");
  }
};

export const handleSearchInput = (e) => {
  setSearchTerm(e.target.value.trim());
  setCurrentPage(1);
  renderAll();
};

export const handleEscapeKey = (e) => {
  if (e.key === "Escape" && getEl("panel").classList.contains("open")) {
    closePanel();
  }
};
