import { getEl } from "../../utils.js";
import { state } from "./state.js";
import { getProducts } from "./api.js";
import { renderAll } from "./render.js";

export const renderPagination = () => {
  getEl("prevPageBtn").disabled = state.currentPage <= 1;
  getEl("nextPageBtn").disabled = state.currentPage >= state.totalPages;
  getEl("paginationPages").innerHTML = buildPageNumbers();
  attachPaginationPageListeners();
};

const buildPageNumbers = () => {
  const pages = getPageNumbersToShow();

  return pages
    .map((page) => {
      if (page === "...") {
        return '<span class="pagination-ellipsis">…</span>';
      }
      const isActive = page === state.currentPage;
      return (
        '<button type="button" class="pagination-page ' +
        (isActive ? "active" : "") +
        '" data-page="' +
        page +
        '">' +
        page +
        "</button>"
      );
    })
    .join("");
};

const getPageNumbersToShow = () => {
  const pages = [];
  const windowSize = 1;

  for (let page = 1; page <= state.totalPages; page++) {
    const isEdge = page === 1 || page === state.totalPages;
    const isNearCurrent = Math.abs(page - state.currentPage) <= windowSize;

    if (isEdge || isNearCurrent) {
      pages.push(page);
    } else if (pages[pages.length - 1] !== "...") {
      pages.push("...");
    }
  }

  return pages;
};

const attachPaginationPageListeners = () => {
  document.querySelectorAll(".pagination-page").forEach((button) => {
    button.addEventListener("click", () =>
      goToPage(Number(button.getAttribute("data-page"))),
    );
  });
};

export const goToPage = async (page) => {
  if (page < 1 || page > state.totalPages || page === state.currentPage) return;
  state.currentPage = page;
  await getProducts(state.currentPage, state.searchTerm);
  renderAll();
};

export const goToPreviousPage = () => goToPage(state.currentPage - 1);
export const goToNextPage = () => goToPage(state.currentPage + 1);
