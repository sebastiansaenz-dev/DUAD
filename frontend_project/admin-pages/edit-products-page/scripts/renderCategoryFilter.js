import { getEl, escapeHtml } from "../../utils.js";
import { state } from "./state.js";
import { getCategoryCounts } from "./dataHelpers.js";
import { renderAll } from "./render.js";

export const renderCategoryFilterList = () => {
  const categoryCounts = getCategoryCounts();
  const listEl = getEl("categoryList");

  listEl.innerHTML =
    buildCategoryFilterButton("all", "All", state.products.length) +
    Object.keys(categoryCounts)
      .sort()
      .map((category) =>
        buildCategoryFilterButton(
          category,
          category,
          categoryCounts[category],
        ),
      )
      .join("");

  attachCategoryFilterListeners();
  refreshCategoryDatalist(categoryCounts);
};

const buildCategoryFilterButton = (value, label, count) => {
  const isActive = state.currentCategoryFilter === value;
  const safeValue = value.replace(/"/g, "&quot;");
  return (
    '<li><button class="filter-btn ' +
    (isActive ? "active" : "") +
    '" data-category="' +
    safeValue +
    '">' +
    "<span>" +
    escapeHtml(label) +
    "</span>" +
    '<span class="filter-count">' +
    count +
    "</span>" +
    "</button></li>"
  );
};

const attachCategoryFilterListeners = () => {
  const buttons = document.querySelectorAll("#categoryList .filter-btn");
  buttons.forEach((button) => {
    button.addEventListener("click", () => handleCategoryFilterClick(button));
  });
};

const handleCategoryFilterClick = (button) => {
  state.currentCategoryFilter = button.getAttribute("data-category");
  renderAll();
};

const refreshCategoryDatalist = (categoryCounts) => {
  const datalist = getEl("categoryOptions");
  datalist.innerHTML = Object.keys(categoryCounts)
    .sort()
    .map(
      (category) =>
        '<option value="' + category.replace(/"/g, "&quot;") + '">',
    )
    .join("");
};
