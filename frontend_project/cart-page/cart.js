import { showUserType } from "../utils/utils.js";
import { activePage } from "../utils/utils.js";
import { checkAuth } from "../utils/utils.js";
import { api } from "../utils/utils.js";

const checkAuthForCart = () => {
  const user = checkAuth();
  if (!user) {
    window.location.href = "../login-page/login.html";
  }
};

const getCart = async () => {
  try {
    const response = await api.get("/cart/");

    if (response.data === "nothing in your cart") {
      displayEmptyCart(response.data);
      return;
    }

    displayCartItems(response.data);
  } catch (error) {
    console.error(error);
  }
};

const displayEmptyCart = (response) => {
  const cartItemsList = document.getElementById("cart-items-list");
  const emptyText = document.createElement("p");
  emptyText.textContent = response;
  cartItemsList.appendChild(emptyText);
};

const displayCartItems = (cartData) => {
  const cartContainer = document.getElementById("cart-items-list");
  const cartTotal = document.getElementById("cart-total");

  cartContainer.innerHTML = "";
  cartTotal.textContent = `$${cartData.total}`;

  cartData.cart_products.forEach((product, index) => {
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
    removeBtn.addEventListener("click", removeProductFromCart);

    cartItem.appendChild(productImageContainer);
    cartItem.appendChild(itemDetailsContainer);
    cartItem.appendChild(removeBtn);

    cartContainer.appendChild(cartItem);
  });
};

const removeProductFromCart = async (event) => {
  const button = event.target;
  const productId = parseInt(button.getAttribute("data-product-id"));

  try {
    await api.delete("/cart/", {
      data: [{ id: productId }],
    });

    getCart();
  } catch (error) {
    console.error("Error removing product:", error);
  }
};

const init = () => {
  checkAuthForCart();
  getCart();
  showUserType();
  activePage();
};

init();
