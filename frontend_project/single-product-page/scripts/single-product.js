import {
  showErrorMessage,
  showUserType,
  checkAuth,
  activePage,
} from "../../utils/utils.js";
import { getProductByIdRequest, addToCartRequest } from "./api.js";
import {
  renderProduct,
  renderProductError,
  showSuccessMessage,
} from "./render.js";
import { attachQuantityStepper } from "./quantitySelector.js";

const getProductIdFromUrl = () => {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
};

const loadProduct = async () => {
  const id = getProductIdFromUrl();
  if (!id) {
    console.error("id not found");
    return;
  }

  try {
    const product = await getProductByIdRequest(id);
    renderProduct(product);
  } catch (error) {
    renderProductError();
    showErrorMessage(error);
  }
};

const addProductToCart = async () => {
  const user = checkAuth();
  if (!user) {
    window.location.href = "../login-page/login.html";
    return;
  }

  const productId = parseInt(getProductIdFromUrl(), 10);
  if (!productId) {
    console.error("Product ID not found");
    return;
  }

  const quantityInput = document.getElementById("quantity-input");
  const quantity = quantityInput ? parseInt(quantityInput.value, 10) : 1;

  try {
    await addToCartRequest(productId, quantity);
    showSuccessMessage("Product added to cart!");
  } catch (error) {
    console.error("Error adding product to cart:", error);
    showErrorMessage(error);
  }
};

const init = () => {
  document
    .getElementById("add-to-cart-button")
    .addEventListener("click", addProductToCart);

  attachQuantityStepper();

  loadProduct();
  showUserType();
  activePage();
};

init();
