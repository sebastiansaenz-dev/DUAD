import { api } from "./axiosClient";

export const syncCartToBackend = async (items) => {
  const { data } = await api.get("/cart/");
  const existing = data?.cart_products ?? [];

  if (existing.length > 0) {
    await api.delete("/cart/", {
      data: existing.map((product) => ({ id: product.id })),
    });
  }

  if (items.length === 0) {
    return;
  }

  return api.post(
    "/cart/",
    items.map((item) => ({
      id: Number(item.id),
      quantity: Number(item.quantity ?? 1),
    })),
  );
};

export const createOrder = (orderData) => {
  return api.post("/orders/", orderData);
};
