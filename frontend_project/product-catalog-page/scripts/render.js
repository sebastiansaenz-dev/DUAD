export const renderProducts = (productsToRender) => {
  const fragment = document.createDocumentFragment();
  const productsContainer = document.getElementById("products-container");
  const noResults = document.getElementById("no-results");

  productsToRender.forEach((product) => {
    fragment.appendChild(buildProductCard(product));
  });

  productsContainer.innerHTML = "";
  productsContainer.appendChild(fragment);
  noResults.hidden = productsToRender.length > 0;
};

const buildProductCard = (product) => {
  const productDiv = document.createElement("div");
  productDiv.classList.add("product");

  const productDataDiv = document.createElement("div");
  productDataDiv.classList.add("product-data-container");

  const productImage = document.createElement("img");
  productImage.classList.add("product-img");
  productImage.src = product.image_url;

  const productTitle = document.createElement("h2");
  productTitle.classList.add("product-name");
  productTitle.textContent = product.name;

  const productPrice = document.createElement("span");
  productPrice.classList.add("product-price");
  productPrice.textContent = `$${product.price}`;

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

  return productDiv;
};

export const renderPagination = (currentPage, totalPages, onPageClick) => {
  const paginationContainer = document.getElementById("pagination-container");
  paginationContainer.innerHTML = "";

  if (totalPages <= 1) return;

  const fragment = document.createDocumentFragment();

  const prevButton = document.createElement("button");
  prevButton.classList.add("pagination-button");
  prevButton.textContent = "«";
  prevButton.disabled = currentPage === 1;
  prevButton.addEventListener("click", () => onPageClick(currentPage - 1));
  fragment.appendChild(prevButton);

  for (let i = 1; i <= totalPages; i++) {
    const pageButton = document.createElement("button");
    pageButton.classList.add("pagination-button");
    if (i === currentPage) pageButton.classList.add("active");
    pageButton.textContent = i;
    pageButton.addEventListener("click", () => onPageClick(i));
    fragment.appendChild(pageButton);
  }

  const nextButton = document.createElement("button");
  nextButton.classList.add("pagination-button");
  nextButton.textContent = "»";
  nextButton.disabled = currentPage === totalPages;
  nextButton.addEventListener("click", () => onPageClick(currentPage + 1));
  fragment.appendChild(nextButton);

  paginationContainer.appendChild(fragment);
};
