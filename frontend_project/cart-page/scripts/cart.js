import {
  showUserType,
  activePage,
  checkAuth,
  showErrorMessage,
} from "../../utils/utils.js";
import { getCartRequest } from "./api.js";
import { renderCart } from "./render.js";
import { removeProductFromCart } from "./handlers.js";

const checkAuthForCart = () => {
  const user = checkAuth();
  if (!user) {
    window.location.href = "../login-page/login.html";
  }
};

const loadCart = async () => {
  try {
    const cartData = await getCartRequest();
    renderCart(cartData);
  } catch (error) {
    showErrorMessage(error);
  }
};

const attachRemoveDelegation = () => {
  const cartItemsList = document.getElementById("cart-items-list");
  cartItemsList.addEventListener("click", (e) => {
    const button = e.target.closest(".remove-btn");
    if (!button) return;

    const productId = parseInt(button.getAttribute("data-product-id"), 10);
    removeProductFromCart(productId, loadCart);
  });
};

const init = () => {
  checkAuthForCart();
  attachRemoveDelegation();
  loadCart();
  showUserType();
  activePage();
};

init();
