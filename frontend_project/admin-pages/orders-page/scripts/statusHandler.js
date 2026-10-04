import { getEl, showToast } from "../../utils.js";
import { state } from "./state.js";
import { findOrderById } from "./dataHelpers.js";
import { updateOrderStatus } from "./api.js";
import { renderAll } from "./render.js";

export const handleSaveStatus = async () => {
  if (!state.selectedOrderId) return;

  const newStatus = getEl("f_status").value;
  const saveBtn = getEl("saveStatusBtn");
  saveBtn.disabled = true;

  try {
    await updateOrderStatus(state.selectedOrderId, newStatus);
    applyStatusToLocalOrder(state.selectedOrderId, newStatus);
    renderAll();
    showToast("Status updated");
  } catch (error) {
    console.error(error);
    showToast("Could not update the status");
  } finally {
    saveBtn.disabled = false;
  }
};

const applyStatusToLocalOrder = (id, newStatus) => {
  const order = findOrderById(id);
  if (order) order.status = newStatus;
};
