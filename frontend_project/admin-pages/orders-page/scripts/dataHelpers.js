import { PAGE_SIZE } from "./constants.js";
import { state } from "./state.js";

export const findOrderById = (id) =>
  state.allOrders.find((order) => order.id === id);

export const getStatusCounts = () => {
  const counts = {};
  state.allOrders.forEach((order) => {
    counts[order.status] = (counts[order.status] || 0) + 1;
  });
  return counts;
};

export const matchesStatusFilter = (order) => {
  return (
    state.currentStatusFilter === "all" ||
    order.status === state.currentStatusFilter
  );
};

export const matchesSearchTerm = (order) => {
  if (!state.searchTerm) return true;
  const term = state.searchTerm.toLowerCase();
  return (
    (order.order_number || "").toLowerCase().includes(term) ||
    (order.full_name || "").toLowerCase().includes(term) ||
    (order.user && order.user.username ? order.user.username : "")
      .toLowerCase()
      .includes(term)
  );
};

export const getFilteredOrders = () => {
  return state.allOrders.filter(
    (order) => matchesStatusFilter(order) && matchesSearchTerm(order),
  );
};

export const getPagedOrders = () => {
  const filtered = getFilteredOrders();
  state.totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  if (state.currentPage > state.totalPages) {
    state.currentPage = state.totalPages;
  }

  const start = (state.currentPage - 1) * PAGE_SIZE;
  return filtered.slice(start, start + PAGE_SIZE);
};
