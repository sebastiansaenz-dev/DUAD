import { api } from "../../utils/utils.js";

export const getProductByIdRequest = async (id) => {
  const response = await api.get(`/products/${id}`);
  return response.data;
};

export const addToCartRequest = async (productId, quantity) => {
  const response = await api.post("/cart/", [{ id: productId, quantity }]);
  return response.data;
};
