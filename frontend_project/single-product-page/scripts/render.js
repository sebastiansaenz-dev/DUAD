export const renderProduct = (product) => {
  document.getElementById("image").src = product.image_url;
  document.getElementById("brand").textContent = product.brand;
  document.getElementById("name").textContent = product.name;
  document.getElementById("price").textContent = `$${product.price}`;
  document.getElementById("description").textContent = product.description;
};

export const renderProductError = () => {
  const productContainer = document.getElementById("product-container");
  productContainer.innerHTML = "";

  const errorSection = document.createElement("div");
  errorSection.classList.add("error-section");
  errorSection.id = "error-section";
  productContainer.appendChild(errorSection);
};

export const showSuccessMessage = (message) => {
  const successDiv = document.getElementById("success-message");
  successDiv.textContent = message;
  successDiv.style.display = "block";

  setTimeout(() => {
    successDiv.style.display = "none";
  }, 3000);
};
