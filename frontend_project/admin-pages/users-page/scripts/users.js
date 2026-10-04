import { protectAdminRoute } from "../../../utils/utils.js";
import { getEl, showToast } from "./helpers.js";
import { getUsers } from "./api.js";
import { setAllUsers } from "./state.js";
import { renderAll, goToPreviousPage, goToNextPage } from "./render.js";
import { openEditPanel, closePanel } from "./panel.js";
import {
  handleFormSubmit,
  handleDeleteClick,
  handleSearchInput,
  handleEscapeKey,
} from "./handlers.js";

protectAdminRoute();

const attachTableActionDelegation = () => {
  getEl("tableBody").addEventListener("click", (e) => {
    const button = e.target.closest("[data-action]");
    if (!button) return;

    const id = Number(button.getAttribute("data-id"));
    if (button.dataset.action === "edit") openEditPanel(id);
    if (button.dataset.action === "delete") handleDeleteClick(id);
  });
};

const globalEventListeners = () => {
  getEl("panelClose").addEventListener("click", closePanel);
  getEl("cancelBtn").addEventListener("click", closePanel);
  getEl("overlay").addEventListener("click", closePanel);
  getEl("userForm").addEventListener("submit", handleFormSubmit);
  getEl("searchInput").addEventListener("input", handleSearchInput);
  getEl("prevPageBtn").addEventListener("click", goToPreviousPage);
  getEl("nextPageBtn").addEventListener("click", goToNextPage);
  document.addEventListener("keydown", handleEscapeKey);
  attachTableActionDelegation();
};

async function loadInitialUsers() {
  try {
    const users = await getUsers();
    setAllUsers(users);
    renderAll();
  } catch (error) {
    console.error(error);
    showToast("Could not load users.");
  }
}

const init = () => {
  globalEventListeners();
  loadInitialUsers();
};

init();
