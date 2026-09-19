import { getEl, formatPrice, escapeHtml } from "../../utils.js";
import { LOW_STOCK_THRESHOLD } from "./constants.js";
import { getFilteredProducts } from "./dataHelpers.js";
import { openEditPanel } from "./panel.js";
import { handleDeleteClick } from "./deleteHandler.js";

export const renderProductTable = () => {
  const visibleProducts = getFilteredProducts();
  const hasResults = visibleProducts.length > 0;

  toggleEmptyState(!hasResults);
  if (!hasResults) {
    getEl("tableBody").innerHTML = "";
    return;
  }

  getEl("tableBody").innerHTML = visibleProducts.map(buildProductRow).join("");
  attachRowActionListeners();
};

const toggleEmptyState = (shouldShow) => {
  getEl("emptyState").style.display = shouldShow ? "block" : "none";
};

const buildProductRow = (product) => {
  const isLowStock = product.stock < LOW_STOCK_THRESHOLD;

  return (
    '<tr data-id="' +
    product.id +
    '">' +
    '<td data-label="Product">' +
    buildProductCell(product) +
    "</td>" +
    '<td data-label="Brand"><span class="tag">' +
    escapeHtml(product.brand) +
    "</span></td>" +
    '<td data-label="Price" class="price">' +
    formatPrice(product.price) +
    "</td>" +
    '<td data-label="Stock">' +
    buildStockPill(product.stock, isLowStock) +
    "</td>" +
    '<td data-label="Actions">' +
    buildRowActions(product.id) +
    "</td>" +
    "</tr>"
  );
};

const buildProductCell = (product) => {
  return (
    '<div class="prod-cell">' +
    buildProductThumbnail(product) +
    "<div>" +
    '<div class="prod-name">' +
    escapeHtml(product.name) +
    "</div>" +
    '<div class="prod-sku">' +
    escapeHtml(product.sku) +
    "</div>" +
    "</div>" +
    "</div>"
  );
};

const buildProductThumbnail = (product) => {
  const backgroundColor = product.color || "#EAE8E2";

  if (!product.image_url) {
    return (
      '<div class="swatch" style="background-color:' +
      backgroundColor +
      '"></div>'
    );
  }

  return (
    '<div class="swatch" style="background-color:' +
    backgroundColor +
    '">' +
    '<img src="' +
    escapeHtml(product.image_url) +
    '" alt="' +
    escapeHtml(product.name) +
    '" onerror="this.remove()">' +
    "</div>"
  );
};

const buildStockPill = (stock, isLowStock) => {
  return (
    '<span class="stock-pill ' +
    (isLowStock ? "low" : "") +
    '">' +
    '<span class="stock-dot"></span>' +
    stock +
    " u." +
    "</span>"
  );
};

const buildRowActions = (productId) => {
  return (
    '<div class="row-actions" style="justify-content:flex-end;">' +
    '<button class="icon-btn" data-action="edit" data-id="' +
    productId +
    '" aria-label="Edit">' +
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>' +
    "</button>" +
    '<button class="icon-btn danger" data-action="delete" data-id="' +
    productId +
    '" aria-label="Delete">' +
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg>' +
    "</button>" +
    "</div>"
  );
};

const attachRowActionListeners = () => {
  document.querySelectorAll('[data-action="edit"]').forEach((button) => {
    button.addEventListener("click", () =>
      openEditPanel(Number(button.getAttribute("data-id"))),
    );
  });
  document.querySelectorAll('[data-action="delete"]').forEach((button) => {
    button.addEventListener("click", () =>
      handleDeleteClick(Number(button.getAttribute("data-id"))),
    );
  });
};
