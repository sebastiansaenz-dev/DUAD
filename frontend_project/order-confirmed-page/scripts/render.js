import { showErrorMessage } from "../../utils/utils.js";

export const displayEmptyCart = (message) => {
  const summaryList = document.querySelector(".summary-items-list");
  const emptyText = document.createElement("p");
  emptyText.textContent = message;
  summaryList.appendChild(emptyText);
};

export const displayOrderSummary = (orderData) => {
  const summaryList = document.querySelector(".summary-items-list");
  const totalPrice = document.querySelector(".total-price");

  if (!orderData) {
    showErrorMessage({ message: "Unable to load order data" });
    displayEmptyCart("Unable to load order data");
    return;
  }

  summaryList.innerHTML = "";

  const products = orderData.cart_products || orderData.items || [];

  if (!Array.isArray(products) || products.length === 0) {
    showErrorMessage("No products found in the order");
    displayEmptyCart("No products in this order");
    return;
  }

  products.forEach((product) => {
    try {
      summaryList.appendChild(buildSummaryItem(product));
    } catch (error) {
      showErrorMessage(error);
    }
  });

  if (totalPrice && orderData.total) {
    totalPrice.textContent = `$${orderData.total.toFixed(2)}`;
  }
};

const buildSummaryItem = (product) => {
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

  return summaryItem;
};
