import {
  showErrorMessage,
  showUserType,
  checkAuth,
  api,
} from "../utils/utils.js";
import { activePage } from "../utils/utils.js";

const getProductById = async () => {
  try {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (!id) {
      console.error("id not found");
      return;
    }

    const response = await api.get(`/products/${id}`);
    const product = response.data;

    document.getElementById("image").src = product.image_url;
    document.getElementById("brand").textContent = product.brand;
    document.getElementById("name").textContent = product.name;
    document.getElementById("price").textContent = `$${product.price}`;
    document.getElementById("description").textContent = product.description;
  } catch (error) {
    const productContainer = document.getElementById("product-container");
    productContainer.innerHTML = "";
    const errorSection = document.createElement("div");
    errorSection.classList.add("error-section");
    errorSection.id = "error-section";
    productContainer.appendChild(errorSection);
    showErrorMessage(error);
  }
};

const addProductToCart = async () => {
  const user = checkAuth();

  if (!user) {
    window.location.href = "../login-page/login.html";
    return;
  }

  try {
    const params = new URLSearchParams(window.location.search);
    const productId = parseInt(params.get("id"), 10);

    if (!productId) {
      console.error("Product ID not found");
      return;
    }

    const quantityInput = document.getElementById("quantity-input");
    const quantity = quantityInput ? parseInt(quantityInput.value) : 1;

    const response = await api.post("/cart/", [
      {
        id: productId,
        quantity: quantity,
      },
    ]);

    showSuccessMessage("Product added to cart!");
    console.log("Product added:", response.data);
  } catch (error) {
    console.error("Error adding product to cart:", error);
    showErrorMessage(error);
  }
};

const showSuccessMessage = (message) => {
  const successDiv = document.getElementById("success-message");
  successDiv.textContent = message;
  successDiv.style.display = "block";

  setTimeout(() => {
    successDiv.style.display = "none";
  }, 3000);
};

const init = () => {
  const addToCartButton = document.getElementById("add-to-cart-button");
  const decreaseButton = document.getElementById("decrease-quantity");
  const increaseButton = document.getElementById("increase-quantity");
  const quantityInput = document.getElementById("quantity-input");

  addToCartButton.addEventListener("click", addProductToCart);

  decreaseButton.addEventListener("click", () => {
    let currentValue = parseInt(quantityInput.value);
    if (currentValue > 1) {
      quantityInput.value = currentValue - 1;
    }
  });

  increaseButton.addEventListener("click", () => {
    let currentValue = parseInt(quantityInput.value);
    if (currentValue < 100) {
      quantityInput.value = currentValue + 1;
    }
  });

  quantityInput.addEventListener("change", () => {
    let value = parseInt(quantityInput.value);
    if (isNaN(value) || value < 1) {
      quantityInput.value = 1;
    } else if (value > 100) {
      quantityInput.value = 100;
    }
  });

  getProductById();
  showUserType();
  activePage();
};

init();
