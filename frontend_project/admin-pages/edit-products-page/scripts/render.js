import { renderBrandFilterList } from "./renderBrandFilter.js";
import { renderProductTable } from "./renderProductTable.js";
import { renderPagination } from "./pagination.js";

export const renderAll = () => {
  renderBrandFilterList();
  renderProductTable();
  renderPagination();
};
