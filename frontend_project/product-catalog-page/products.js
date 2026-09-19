import { showUserType, apiPublic } from "../utils/utils.js";
import { activePage } from "../utils/utils.js";
import { showErrorMessage } from "../utils/utils.js";

let products = [];
let currentPage = 1;
let totalPages = 1;
let debounceTimer = null;

const renderPagination = () => {
  const paginationContainer = document.getElementById("pagination-container");
  paginationContainer.innerHTML = "";

  if (totalPages <= 1) return;

  const fragment = document.createDocumentFragment();

  const prevButton = document.createElement("button");
  prevButton.classList.add("pagination-button");
  prevButton.textContent = "«";
  prevButton.disabled = currentPage === 1;
  prevButton.addEventListener("click", () => goToPage(currentPage - 1));
  fragment.appendChild(prevButton);

  for (let i = 1; i <= totalPages; i++) {
    const pageButton = document.createElement("button");
    pageButton.classList.add("pagination-button");
    if (i === currentPage) pageButton.classList.add("active");
    pageButton.textContent = i;
    pageButton.addEventListener("click", () => goToPage(i));
    fragment.appendChild(pageButton);
  }

  const nextButton = document.createElement("button");
  nextButton.classList.add("pagination-button");
  nextButton.textContent = "»";
  nextButton.disabled = currentPage === totalPages;
  nextButton.addEventListener("click", () => goToPage(currentPage + 1));
  fragment.appendChild(nextButton);

  paginationContainer.appendChild(fragment);
};

const goToPage = (page) => {
  if (page < 1 || page > totalPages || page === currentPage) return;
  currentPage = page;
  getProducts(currentPage);
  window.scrollTo({ top: 0, behavior: "smooth" });
};

const renderProducts = (productsToRender) => {
  const fragment = document.createDocumentFragment();
  const productsContainer = document.getElementById("products-container");
  const noResults = document.getElementById("no-results");

  productsToRender.forEach((product) => {
    const productDiv = document.createElement("div");
    productDiv.classList.add("product");

    const productDataDiv = document.createElement("div");
    productDataDiv.classList.add("product-data-container");

    // product image
    const productImage = document.createElement("img");
    productImage.classList.add("product-img");
    productImage.src = product.image_url;

    // product data

    // title
    const productTitle = document.createElement("h2");
    productTitle.classList.add("product-name");
    productTitle.textContent = product.name;

    // price
    const productPrice = document.createElement("span");
    productPrice.classList.add("product-price");
    productPrice.textContent = `$${product.price}`;

    // brand

    const productBrand = document.createElement("p");
    productBrand.classList.add("product-brand");
    productBrand.textContent = product.brand;

    const viewDetailsButton = document.createElement("button");
    viewDetailsButton.classList.add("view-details-button");
    viewDetailsButton.dataset.id = product.id;
    viewDetailsButton.textContent = "View details";

    productDataDiv.appendChild(productTitle);
    productDataDiv.appendChild(productPrice);
    productDataDiv.appendChild(productBrand);
    productDiv.appendChild(productImage);
    productDiv.appendChild(productDataDiv);
    productDiv.appendChild(viewDetailsButton);
    fragment.appendChild(productDiv);
  });

  productsContainer.innerHTML = "";
  productsContainer.appendChild(fragment);
  noResults.hidden = productsToRender.length > 0;
};

const filterProducts = (e) => {
  const searchTerm = e.target.value.trim();
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    currentPage = 1;
    getProducts(currentPage, searchTerm);
  }, 350);
};

const getProducts = async (page = 1, search = "") => {
  try {
    let url = `/products/?page=${page}`;
    if (search) {
      url += `&name=${encodeURIComponent(search)}`;
    }
    const response = await apiPublic.get(url);
    products = response.data.items;
    currentPage = response.data.page;
    totalPages = response.data.total_pages;
    renderProducts(products);
    renderPagination();
  } catch (error) {
    showErrorMessage(error);
  }
};

const init = () => {
  document
    .getElementById("product-search-input")
    .addEventListener("input", filterProducts);

  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("view-details-button")) {
      const id = e.target.dataset.id;
      window.location.href = `../single-product-page/single-product.html?id=${id}`;
    }
  });

  getProducts();
  showUserType();
  activePage();
};

init();
