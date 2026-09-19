import {
  showUserType,
  activePage,
  checkAuth,
  showErrorMessage,
} from "../../utils/utils.js";
import { getCartRequest, submitOrderRequest } from "./api.js";
import { displayEmptyCart, displayOrderSummary } from "./render.js";
import { readOrderForm, isOrderFormValid } from "./form.js";

const checkAuthForOrderSummary = () => {
  const user = checkAuth();
  if (!user) {
    window.location.href = "../login-page/login.html";
  }
};

const loadCart = async () => {
  try {
    const cartData = await getCartRequest();

    if (!cartData?.cart_products?.length) {
      displayEmptyCart("nothing in your cart");
      return;
    }

    displayOrderSummary(cartData);
  } catch (error) {
    showErrorMessage(error);
  }
};

const submitOrder = async (event) => {
  event.preventDefault();

  const orderData = readOrderForm();

  if (!isOrderFormValid(orderData)) {
    showErrorMessage({ message: "Please complete all the fields" });
    return;
  }

  try {
    const order = await submitOrderRequest(orderData);

    if (order) {
      sessionStorage.setItem("lastOrder", JSON.stringify(order));
    }

    window.location.href = "../order-confirmed-page/order-confirmed.html";
  } catch (error) {
    showErrorMessage(error);
  }
};

const init = () => {
  checkAuthForOrderSummary();
  loadCart();
  showUserType();
  activePage();

  const orderForm = document.getElementById("order-form");
  if (orderForm) {
    orderForm.addEventListener("submit", submitOrder);
  }
};

init();
