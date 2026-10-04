import { getEl } from "../../utils.js";
import { SEARCH_DEBOUNCE_MS } from "./constants.js";
import { state } from "./state.js";
import { getProducts } from "./api.js";
import { renderAll } from "./render.js";
import { closePanel } from "./panel.js";

export const handleSearchInput = (e) => {
  state.searchTerm = e.target.value.trim();

  clearTimeout(state.searchDebounceTimer);
  state.searchDebounceTimer = setTimeout(async () => {
    state.currentPage = 1;
    await getProducts(state.currentPage, state.searchTerm);
    renderAll();
  }, SEARCH_DEBOUNCE_MS);
};

export const handleEscapeKey = (e) => {
  if (e.key === "Escape" && getEl("panel").classList.contains("open")) {
    closePanel();
  }
};
