import { api } from "../../utils/utils.js";

export const getCartRequest = async () => {
  const response = await api.get("/cart/");
  return response.data;
};

export const submitOrderRequest = async (orderData) => {
  const response = await api.post("/orders/", orderData);
  return response.data;
};
