import {
  getEl,
  formatPrice,
  formatDate,
  escapeHtml,
  statusToClassName,
} from "../../utils.js";
import { getPagedOrders } from "./dataHelpers.js";
import { openOrderDetailPanel } from "./panel.js";

export const renderOrdersTable = () => {
  const visibleOrders = getPagedOrders();
  const hasResults = visibleOrders.length > 0;

  toggleEmptyState(!hasResults);
  if (!hasResults) {
    getEl("tableBody").innerHTML = "";
    return;
  }

  getEl("tableBody").innerHTML = visibleOrders.map(buildOrderRow).join("");
  attachRowActionListeners();
};

const toggleEmptyState = (shouldShow) => {
  getEl("emptyState").style.display = shouldShow ? "block" : "none";
};

const buildOrderRow = (order) => {
  return (
    '<tr data-id="' +
    order.id +
    '">' +
    '<td data-label="Order"><span class="prod-sku">' +
    escapeHtml(order.order_number) +
    "</span></td>" +
    '<td data-label="Customer">' +
    escapeHtml(order.full_name || "—") +
    "</td>" +
    '<td data-label="Date">' +
    formatDate(order.date) +
    "</td>" +
    '<td data-label="Status">' +
    buildStatusPill(order.status) +
    "</td>" +
    '<td data-label="Total" class="price">' +
    formatPrice(order.total) +
    "</td>" +
    '<td data-label="Actions">' +
    buildRowActions(order.id) +
    "</td>" +
    "</tr>"
  );
};

const buildStatusPill = (status) => {
  return (
    '<span class="status-pill ' +
    statusToClassName(status) +
    '">' +
    escapeHtml(status || "Unknown") +
    "</span>"
  );
};

const buildRowActions = (orderId) => {
  return (
    '<div class="row-actions" style="justify-content:flex-end;">' +
    '<button class="icon-btn" data-action="view" data-id="' +
    orderId +
    '" aria-label="View order">' +
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7Z"/><circle cx="12" cy="12" r="3"/></svg>' +
    "</button>" +
    "</div>"
  );
};

const attachRowActionListeners = () => {
  document.querySelectorAll('[data-action="view"]').forEach((button) => {
    button.addEventListener("click", () =>
      openOrderDetailPanel(Number(button.getAttribute("data-id"))),
    );
  });
};
