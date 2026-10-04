import { getEl, formatPrice, formatDate, escapeHtml } from "../../utils.js";
import { statusOptions } from "./constants.js";
import { state } from "./state.js";
import { findOrderById } from "./dataHelpers.js";

export const openOrderDetailPanel = (orderId) => {
  const order = findOrderById(orderId);
  if (!order) return;

  fillOrderDetail(order);
  openPanel();
};

const fillOrderDetail = (order) => {
  state.selectedOrderId = order.id;
  getEl("panelTitle").textContent = "Order " + order.order_number;
  getEl("orderMeta").innerHTML = buildOrderMeta(order);
  renderStatusSelected(order.status);

  const items = order.items || [];
  getEl("orderItemsBody").innerHTML = items.map(buildOrderItemRow).join("");
  getEl("orderTotal").innerHTML =
    "<span>Total</span><span>" + formatPrice(order.total) + "</span>";
};

const renderStatusSelected = (currentStatus) => {
  const select = getEl("f_status");
  const options = statusOptions.includes(currentStatus)
    ? statusOptions
    : [currentStatus, ...statusOptions];

  select.innerHTML = options
    .map(
      (status) =>
        '<option value="' +
        escapeHtml(status) +
        '">' +
        escapeHtml(status) +
        "</option>",
    )
    .join("");
  select.value = currentStatus;
};

const buildOrderMeta = (order) => {
  const rows = [
    ["Customer", order.full_name || "—"],
    ["Username", order.user ? order.user.username : "—"],
    ["Phone", order.phone || "—"],
    ["Address", order.address || "—"],
    ["Date", formatDate(order.date)],
    ["Payment method", order.payment_method_name || "—"],
  ];

  return rows.map(buildOrderMetaRow).join("");
};

const buildOrderMetaRow = ([label, value]) => {
  return (
    '<div class="order-meta-row">' +
    '<span class="order-meta-label">' +
    escapeHtml(label) +
    "</span>" +
    '<span class="order-meta-value">' +
    escapeHtml(String(value)) +
    "</span>" +
    "</div>"
  );
};

const buildOrderItemRow = (item) => {
  return (
    "<tr>" +
    '<td data-label="Product">' +
    buildOrderItemCell(item) +
    "</td>" +
    '<td data-label="Qty">' +
    item.quantity +
    "</td>" +
    '<td data-label="Unit price" class="price">' +
    formatPrice(item.price_at_purchase) +
    "</td>" +
    '<td data-label="Subtotal" class="price" style="text-align:right;">' +
    formatPrice(item.total) +
    "</td>" +
    "</tr>"
  );
};

const buildOrderItemCell = (item) => {
  const thumbnail = item.image_url
    ? '<div class="swatch"><img src="' +
      escapeHtml(item.image_url) +
      '" alt="' +
      escapeHtml(item.product_name) +
      '" onerror="this.remove()"></div>'
    : '<div class="swatch"></div>';

  return (
    '<div class="prod-cell">' +
    thumbnail +
    '<div class="prod-name">' +
    escapeHtml(item.product_name) +
    "</div>" +
    "</div>"
  );
};

const openPanel = () => {
  getEl("overlay").classList.add("open");
  getEl("panel").classList.add("open");
};

export const closePanel = () => {
  getEl("overlay").classList.remove("open");
  getEl("panel").classList.remove("open");
  state.selectedOrderId = null;
};
