export const readOrderForm = () => {
  return {
    full_name: document.getElementById("name").value,
    address: document.getElementById("address").value,
    phone: document.getElementById("phone").value,
    payment_method: document.getElementById("payment").value,
  };
};

export const isOrderFormValid = (orderData) => {
  return (
    Boolean(orderData.full_name) &&
    Boolean(orderData.address) &&
    Boolean(orderData.phone)
  );
};
