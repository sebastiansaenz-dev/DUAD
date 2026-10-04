import { getEl } from "../../utils.js";
import { state } from "./state.js";
import { findProductById } from "./dataHelpers.js";

export const openCreatePanel = () => {
  state.editingProductId = null;
  resetForm();
  setPanelTitle("New product");
  setSaveButtonLabel("Save product");
  openPanel();
};

export const openEditPanel = (productId) => {
  const product = findProductById(productId);
  if (!product) return;

  state.editingProductId = productId;
  resetForm();
  fillFormWithProduct(product);
  setPanelTitle("Edit product");
  setSaveButtonLabel("Save changes");
  openPanel();
};

const setPanelTitle = (title) => {
  getEl("panelTitle").textContent = title;
};

const setSaveButtonLabel = (label) => {
  getEl("saveBtn").textContent = label;
};

const resetForm = () => {
  getEl("productForm").reset();
};

const fillFormWithProduct = (product) => {
  getEl("f_name").value = product.name;
  getEl("f_brand").value = product.brand;
  getEl("f_sku").value = product.sku;
  getEl("f_image_url").value = product.image_url || "";
  getEl("f_price").value = product.price;
  getEl("f_stock").value = product.stock;
  getEl("f_description").value = product.description || "";
};

const openPanel = () => {
  getEl("overlay").classList.add("open");
  getEl("panel").classList.add("open");
  setTimeout(() => getEl("f_name").focus(), 300);
};

export const closePanel = () => {
  getEl("overlay").classList.remove("open");
  getEl("panel").classList.remove("open");
  state.editingProductId = null;
};
