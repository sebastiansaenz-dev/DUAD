export const renderCart = (cartData) => {
  if (cartData.cart_products.length === 0) {
    renderEmptyCart("nothing in your cart");
    return;
  }
  renderCartItems(cartData);
};

const renderEmptyCart = (message) => {
  const cartItemsList = document.getElementById("cart-items-list");
  cartItemsList.innerHTML = "";

  const emptyText = document.createElement("p");
  emptyText.textContent = message;
  cartItemsList.appendChild(emptyText);
};

const renderCartItems = (cartData) => {
  const cartContainer = document.getElementById("cart-items-list");
  const cartTotal = document.getElementById("cart-total");

  cartContainer.innerHTML = "";
  cartTotal.textContent = `$${cartData.total}`;

  cartData.cart_products.forEach((product) => {
    cartContainer.appendChild(buildCartItemElement(product));
  });
};

const buildCartItemElement = (product) => {
  const cartItem = document.createElement("div");
  cartItem.className = "cart-item";

  const productImageContainer = document.createElement("div");
  productImageContainer.className = "product-img";

  const productImage = document.createElement("img");
  productImage.src = product.image_url;
  productImage.alt = product.name;
  productImageContainer.appendChild(productImage);

  const itemDetailsContainer = document.createElement("div");
  itemDetailsContainer.className = "cart-item-details";

  const itemName = document.createElement("h4");
  itemName.textContent = product.name;
  itemDetailsContainer.appendChild(itemName);

  const itemQuantityPrice = document.createElement("p");
  itemQuantityPrice.textContent = `Quantity: ${product.quantity} | Price: $${product.price.toFixed(2)}`;
  itemDetailsContainer.appendChild(itemQuantityPrice);

  const itemTotal = document.createElement("p");
  itemTotal.className = "item-total";
  itemTotal.textContent = `Total: $${product.total.toFixed(2)}`;
  itemDetailsContainer.appendChild(itemTotal);

  const removeBtn = document.createElement("button");
  removeBtn.className = "remove-btn";
  removeBtn.textContent = "Remove";
  removeBtn.setAttribute("data-product-id", product.id);

  cartItem.appendChild(productImageContainer);
  cartItem.appendChild(itemDetailsContainer);
  cartItem.appendChild(removeBtn);

  return cartItem;
};
