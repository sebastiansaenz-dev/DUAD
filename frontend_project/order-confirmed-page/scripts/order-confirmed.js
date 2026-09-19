import {
  showUserType,
  activePage,
  checkAuth,
  showErrorMessage,
} from "../utils/utils.js";
import { displayOrderSummary } from "./render.js";

const checkAuthForOrderConfirmed = () => {
  const user = checkAuth();
  if (!user) {
    window.location.href = "../login-page/login.html";
  }
};

const getOrderData = () => {
  try {
    const savedOrder = sessionStorage.getItem("lastOrder");

    if (!savedOrder) {
      window.location.href = "../product-catalog-page/products.html";
      return;
    }

    const orderData = JSON.parse(savedOrder);
    displayOrderSummary(orderData);

    sessionStorage.removeItem("lastOrder");
  } catch (error) {
    showErrorMessage(error);
    window.location.href = "../product-catalog-page/products.html";
  }
};

const init = () => {
  checkAuthForOrderConfirmed();
  getOrderData();
  showUserType();
  activePage();
};

init();
