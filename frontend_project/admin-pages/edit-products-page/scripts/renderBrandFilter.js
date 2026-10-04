import { getEl, escapeHtml } from "../../utils.js";
import { state } from "./state.js";
import { getBrandCounts } from "./dataHelpers.js";
import { renderAll } from "./render.js";

export const renderBrandFilterList = () => {
  const brandCounts = getBrandCounts();
  const listEl = getEl("brandList");

  listEl.innerHTML =
    buildBrandFilterButton("all", "All", state.products.length) +
    Object.keys(brandCounts)
      .sort()
      .map((brand) => buildBrandFilterButton(brand, brand, brandCounts[brand]))
      .join("");

  attachBrandFilterListeners();
  refreshBrandDatalist(brandCounts);
};

const buildBrandFilterButton = (value, label, count) => {
  const isActive = state.currentBrandFilter === value;
  const safeValue = value.replace(/"/g, "&quot;");
  return (
    '<li><button class="filter-btn ' +
    (isActive ? "active" : "") +
    '" data-brand="' +
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

const attachBrandFilterListeners = () => {
  const buttons = document.querySelectorAll("#brandList .filter-btn");
  buttons.forEach((button) => {
    button.addEventListener("click", () => handleBrandFilterClick(button));
  });
};

const handleBrandFilterClick = (button) => {
  state.currentBrandFilter = button.getAttribute("data-brand");
  renderAll();
};

const refreshBrandDatalist = (brandCounts) => {
  const datalist = getEl("brandOptions");
  datalist.innerHTML = Object.keys(brandCounts)
    .sort()
    .map((brand) => '<option value="' + brand.replace(/"/g, "&quot;") + '">')
    .join("");
};
