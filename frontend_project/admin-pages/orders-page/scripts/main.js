import { protectAdminRoute } from "../../../utils/utils.js";
import { getEl, showToast } from "../../utils.js";
import { getOrders } from "./api.js";
import { renderAll } from "./render.js";
import { closePanel } from "./panel.js";
import { handleSaveStatus } from "./statusHandler.js";
import { handleSearchInput, handleEscapeKey } from "./search.js";
import { goToPreviousPage, goToNextPage } from "./pagination.js";

protectAdminRoute();

async function loadInitialOrders() {
  try {
    await getOrders();
    renderAll();
  } catch (error) {
    console.error(error);
    showToast("Could not load orders.");
  }
}

const globalEventListeners = () => {
  getEl("panelClose").addEventListener("click", closePanel);
  getEl("closeDetailBtn").addEventListener("click", closePanel);
  getEl("saveStatusBtn").addEventListener("click", handleSaveStatus);
  getEl("overlay").addEventListener("click", closePanel);
  getEl("searchInput").addEventListener("input", handleSearchInput);
  getEl("prevPageBtn").addEventListener("click", goToPreviousPage);
  getEl("nextPageBtn").addEventListener("click", goToNextPage);
  document.addEventListener("keydown", handleEscapeKey);
};

const init = () => {
  globalEventListeners();
  loadInitialOrders();
};

init();
