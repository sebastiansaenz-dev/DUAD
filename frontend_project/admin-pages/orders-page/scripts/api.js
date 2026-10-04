import { api } from "../../../utils/utils.js";
import { state } from "./state.js";

// GET
export const getOrders = async () => {
  try {
    const response = await api.get("/orders/");
    state.allOrders = Array.isArray(response.data) ? response.data : [];
    return state.allOrders;
  } catch (error) {
    console.error(error);
    return [];
  }
};

// UPDATE
export const updateOrderStatus = async (id, status) => {
  const url = `/staff-portal/orders/${id}`;
  const response = await api.patch(url, {
    status: status,
  });
  return response.data;
};
