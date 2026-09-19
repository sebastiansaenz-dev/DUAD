import {
  showUserType,
  activePage,
  showErrorMessage,
} from "../../utils/utils.js";
import { getProductsRequest } from "./api.js";
import { renderProducts, renderPagination } from "./render.js";

let currentPage = 1;
let totalPages = 1;
let currentSearch = "";
let debounceTimer = null;

const loadProducts = async (page = 1, search = "") => {
  try {
    const data = await getProductsRequest(page, search);
    currentPage = data.page;
    totalPages = data.total_pages;
    renderProducts(data.items);
    renderPagination(currentPage, totalPages, goToPage);
  } catch (error) {
    showErrorMessage(error);
  }
};

const goToPage = (page) => {
  if (page < 1 || page > totalPages || page === currentPage) return;
  loadProducts(page, currentSearch);
  window.scrollTo({ top: 0, behavior: "smooth" });
};

const handleSearchInput = (e) => {
  currentSearch = e.target.value.trim();
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    loadProducts(1, currentSearch);
  }, 350);
};

const attachViewDetailsDelegation = () => {
  document.addEventListener("click", (e) => {
    if (!e.target.classList.contains("view-details-button")) return;
    const id = e.target.dataset.id;
    window.location.href = `../single-product-page/single-product.html?id=${id}`;
  });
};

const init = () => {
  document
    .getElementById("product-search-input")
    .addEventListener("input", handleSearchInput);

  attachViewDetailsDelegation();

  loadProducts();
  showUserType();
  activePage();
};

init();
