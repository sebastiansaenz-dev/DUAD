import { api } from "../../utils/utils.js";

export const getCartRequest = async () => {
  const response = await api.get("/cart/");
  return response.data;
};

export const removeFromCartRequest = async (productId) => {
  await api.delete("/cart/", {
    data: [{ id: productId }],
  });
};
