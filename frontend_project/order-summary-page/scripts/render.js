export const displayEmptyCart = (message) => {
  const summaryList = document.querySelector(".summary-items-list");
  const emptyText = document.createElement("p");
  emptyText.textContent = message;
  summaryList.appendChild(emptyText);
};

export const displayOrderSummary = (cartData) => {
  const summaryList = document.querySelector(".summary-items-list");
  const totalPrice = document.querySelector(".total-price");

  summaryList.innerHTML = "";

  cartData.cart_products.forEach((product) => {
    summaryList.appendChild(buildSummaryItem(product));
  });

  if (totalPrice) {
    totalPrice.textContent = `$${cartData.total.toFixed(2)}`;
  }
};

const buildSummaryItem = (product) => {
  const summaryItem = document.createElement("div");
  summaryItem.className = "summary-item";

  const productImage = document.createElement("img");
  productImage.src = product.image_url;
  productImage.alt = product.name;

  const itemDetailsContainer = document.createElement("div");
  itemDetailsContainer.className = "summary-item-details";

  const itemName = document.createElement("h4");
  itemName.textContent = product.name;
  itemDetailsContainer.appendChild(itemName);

  const itemQuantity = document.createElement("p");
  itemQuantity.textContent = `Cantidad: ${product.quantity}`;
  itemDetailsContainer.appendChild(itemQuantity);

  const itemPrice = document.createElement("span");
  itemPrice.className = "summary-item-price";
  itemPrice.textContent = `$${product.total.toFixed(2)}`;

  summaryItem.appendChild(productImage);
  summaryItem.appendChild(itemDetailsContainer);
  summaryItem.appendChild(itemPrice);

  return summaryItem;
};
