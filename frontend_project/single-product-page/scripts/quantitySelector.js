export const attachQuantityStepper = () => {
  const decreaseButton = document.getElementById("decrease-quantity");
  const increaseButton = document.getElementById("increase-quantity");
  const quantityInput = document.getElementById("quantity-input");

  decreaseButton.addEventListener("click", () => {
    const currentValue = parseInt(quantityInput.value, 10);
    if (currentValue > 1) {
      quantityInput.value = currentValue - 1;
    }
  });

  increaseButton.addEventListener("click", () => {
    const currentValue = parseInt(quantityInput.value, 10);
    if (currentValue < 100) {
      quantityInput.value = currentValue + 1;
    }
  });

  quantityInput.addEventListener("change", () => {
    const value = parseInt(quantityInput.value, 10);
    if (isNaN(value) || value < 1) {
      quantityInput.value = 1;
    } else if (value > 100) {
      quantityInput.value = 100;
    }
  });
};
