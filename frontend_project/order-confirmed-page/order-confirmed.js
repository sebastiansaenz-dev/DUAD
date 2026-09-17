import { showUserType } from "../utils/utils.js";
import { activePage } from "../utils/utils.js";
import { checkAuth } from "../utils/utils.js";
import { api } from "../utils/utils.js";

const checkAuthForOrderConfirmed = () => {
  const user = checkAuth();
  if (!user) {
    window.location.href = "../login-page/login.html";
  }
};

const getOrderData = async () => {
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
    console.error(error);
    window.location.href = "../product-catalog-page/products.html";
  }
};

const displayEmptyCart = (response) => {
  const summaryList = document.querySelector(".summary-items-list");
  const emptyText = document.createElement("p");
  emptyText.textContent = response;
  summaryList.appendChild(emptyText);
};

const displayOrderSummary = (orderData) => {
  const summaryList = document.querySelector(".summary-items-list");
  const totalPrice = document.querySelector(".total-price");

  if (!orderData) {
    console.error("Order data is undefined");
    displayEmptyCart("Unable to load order data");
    return;
  }

  summaryList.innerHTML = "";

  const products = orderData.cart_products || orderData.items || [];

  if (!Array.isArray(products) || products.length === 0) {
    console.warn("No products found in order data:", orderData);
    displayEmptyCart("No products in this order");
    return;
  }

  products.forEach((product) => {
    try {
      const summaryItem = document.createElement("div");
      summaryItem.className = "summary-item";

      const productImage = document.createElement("img");
      productImage.src = product.image_url || "";
      productImage.alt = product.name || product.product_name || "Product";

      const itemDetailsContainer = document.createElement("div");
      itemDetailsContainer.className = "summary-item-details";

      const itemName = document.createElement("h4");
      itemName.textContent =
        product.name || product.product_name || "Unknown Product";
      itemDetailsContainer.appendChild(itemName);

      const itemQuantity = document.createElement("p");
      itemQuantity.textContent = `Quantity: ${product.quantity || 0}`;
      itemDetailsContainer.appendChild(itemQuantity);

      const itemPrice = document.createElement("span");
      itemPrice.className = "summary-item-price";
      const totalAmount =
        product.total || product.price_at_purchase * product.quantity;
      itemPrice.textContent = `$${totalAmount.toFixed(2)}`;

      summaryItem.appendChild(productImage);
      summaryItem.appendChild(itemDetailsContainer);
      summaryItem.appendChild(itemPrice);

      summaryList.appendChild(summaryItem);
    } catch (error) {
      console.error("Error displaying product:", product, error);
    }
  });

  if (totalPrice && orderData.total) {
    totalPrice.textContent = `$${orderData.total.toFixed(2)}`;
  }
};

const init = () => {
  checkAuthForOrderConfirmed();
  getOrderData();
  showUserType();
  activePage();
};

init();
