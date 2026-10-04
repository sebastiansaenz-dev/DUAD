import { renderStatusFilterList } from "./renderStatusFilter.js";
import { renderOrdersTable } from "./renderOrdersTable.js";
import { renderPagination } from "./pagination.js";

export const renderAll = () => {
  renderStatusFilterList();
  renderOrdersTable();
  renderPagination();
};
