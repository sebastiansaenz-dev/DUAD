import { renderCategoryFilterList } from "./renderCategoryFilter.js";
import { renderProductTable } from "./renderProductTable.js";
import { renderPagination } from "./pagination.js";

export const renderAll = () => {
  renderCategoryFilterList();
  renderProductTable();
  renderPagination();
};
