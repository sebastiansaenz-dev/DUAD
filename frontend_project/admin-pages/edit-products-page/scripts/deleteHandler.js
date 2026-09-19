import { showToast } from "../../utils.js";
import { state } from "./state.js";
import { findProductById } from "./dataHelpers.js";
import { getProducts, deleteProductRequest } from "./api.js";
import { renderAll } from "./render.js";

export const handleDeleteClick = async (id) => {
  const product = findProductById(id);
  if (!product) return;

  const confirmed = confirm('Remove "' + product.name + '" from the catalog?');
  if (!confirmed) return;

  const row = document.querySelector('tr[data-id="' + id + '"]');
  if (row) row.classList.add("fading");

  try {
    await deleteProductRequest(id);
    setTimeout(() => finishDelete(id), row ? 220 : 0);
  } catch (error) {
    console.error(error);
    if (row) row.classList.remove("fading");
    showToast("Could not delete the product.");
  }
};

const finishDelete = async (id) => {
  await getProducts(state.currentPage, state.searchTerm);
  renderAll();
  showToast("Product deleted.");
};
