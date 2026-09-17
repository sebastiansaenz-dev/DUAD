import { showUserType } from "../utils/utils.js";
import { activePage } from "../utils/utils.js";
import { checkAuth } from "../utils/utils.js";
import { api } from "../utils/utils.js";

const checkAuthForOrderSummary = () => {
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

    displayOrderSummary(response.data);
  } catch (error) {
    console.error(error);
  }
};

const displayEmptyCart = (response) => {
  const summaryList = document.querySelector(".summary-items-list");
  const emptyText = document.createElement("p");
  emptyText.textContent = response;
  summaryList.appendChild(emptyText);
};

const displayOrderSummary = (cartData) => {
  const summaryList = document.querySelector(".summary-items-list");
  const totalPrice = document.querySelector(".total-price");

  summaryList.innerHTML = "";

  cartData.cart_products.forEach((product) => {
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

    summaryList.appendChild(summaryItem);
  });

  if (totalPrice) {
    totalPrice.textContent = `$${cartData.total.toFixed(2)}`;
  }
};

const submitOrder = async (event) => {
  event.preventDefault();

  const name = document.getElementById("name").value;
  const address = document.getElementById("address").value;
  const phone = document.getElementById("phone").value;
  const payment = document.getElementById("payment").value;

  if (!name || !address || !phone) {
    alert("Please complete all the fields");
    return;
  }

  try {
    const orderData = {
      full_name: name,
      address: address,
      phone: phone,
      payment_method: payment,
    };

    const response = await api.post("/orders/", orderData);

    console.log("Order created successfully:", response.data);

    if (response.data) {
      sessionStorage.setItem("lastOrder", JSON.stringify(response.data));
      console.log("Order saved to sessionStorage");
    }

    window.location.href = "../order-confirmed-page/order-confirmed.html";
  } catch (error) {
    console.error("There was an error creating the order:", error);
    alert(
      "Error creating the order: " +
        (error.response?.data?.message || error.message),
    );
  }
};

const init = () => {
  checkAuthForOrderSummary();
  getCart();
  showUserType();
  activePage();

  const orderForm = document.getElementById("order-form");
  if (orderForm) {
    orderForm.addEventListener("submit", submitOrder);
  }
};

init();
