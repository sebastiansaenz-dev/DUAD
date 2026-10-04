import { getEl, escapeHtml } from "../../utils.js";
import { state } from "./state.js";
import { getStatusCounts } from "./dataHelpers.js";
import { renderAll } from "./render.js";

export const renderStatusFilterList = () => {
  const statusCounts = getStatusCounts();
  const listEl = getEl("statusList");

  listEl.innerHTML =
    buildStatusFilterButton("all", "All", state.allOrders.length) +
    Object.keys(statusCounts)
      .sort()
      .map((status) =>
        buildStatusFilterButton(status, status, statusCounts[status]),
      )
      .join("");

  attachStatusFilterListeners();
};

const buildStatusFilterButton = (value, label, count) => {
  const isActive = state.currentStatusFilter === value;
  const safeValue = value.replace(/"/g, "&quot;");
  return (
    '<li><button class="filter-btn ' +
    (isActive ? "active" : "") +
    '" data-status="' +
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

const attachStatusFilterListeners = () => {
  document.querySelectorAll("#statusList .filter-btn").forEach((button) => {
    button.addEventListener("click", () => handleStatusFilterClick(button));
  });
};

const handleStatusFilterClick = (button) => {
  state.currentStatusFilter = button.getAttribute("data-status");
  state.currentPage = 1;
  renderAll();
};
