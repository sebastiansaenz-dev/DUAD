import { getEl } from "../../utils.js";
import { state } from "./state.js";
import { renderAll } from "./render.js";
import { closePanel } from "./panel.js";

export const handleSearchInput = (e) => {
  state.searchTerm = e.target.value.trim();
  state.currentPage = 1;
  renderAll();
};

export const handleEscapeKey = (e) => {
  if (e.key === "Escape" && getEl("panel").classList.contains("open")) {
    closePanel();
  }
};
