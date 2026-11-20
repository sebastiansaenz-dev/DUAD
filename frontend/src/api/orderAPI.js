import { api } from "./axiosClient";

export const createOrder = (orderData) => {
  return api.post("/orders/", orderData);
};
