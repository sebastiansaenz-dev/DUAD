import { protectAdminRoute } from "../../../utils/utils.js";
import { getEl, showToast } from "../../utils.js";
import { state } from "./state.js";
import { getProducts } from "./api.js";
import { renderAll } from "./render.js";
import { openCreatePanel, closePanel } from "./panel.js";
import { handleFormSubmit } from "./form.js";
import { handleSearchInput, handleEscapeKey } from "./search.js";
import { goToPreviousPage, goToNextPage } from "./pagination.js";

protectAdminRoute();

const loadInitialProducts = async () => {
  try {
    await getProducts(state.currentPage);
    renderAll();
  } catch (error) {
    console.error(error);
    showToast("Could not load products.");
  }
};

const globalEventListeners = () => {
  getEl("addBtn").addEventListener("click", openCreatePanel);
  getEl("emptyAddBtn").addEventListener("click", openCreatePanel);
  getEl("panelClose").addEventListener("click", closePanel);
  getEl("cancelBtn").addEventListener("click", closePanel);
  getEl("overlay").addEventListener("click", closePanel);
  getEl("productForm").addEventListener("submit", handleFormSubmit);
  getEl("searchInput").addEventListener("input", handleSearchInput);
  getEl("prevPageBtn").addEventListener("click", goToPreviousPage);
  getEl("nextPageBtn").addEventListener("click", goToNextPage);
  document.addEventListener("keydown", handleEscapeKey);
};

const init = () => {
  globalEventListeners();
  loadInitialProducts();
};

init();
