import { getEl, showToast } from "../../utils.js";
import { state } from "./state.js";
import { findProductById } from "./dataHelpers.js";
import { createProductRequest, updateProductRequest } from "./api.js";
import { closePanel } from "./panel.js";
import { renderAll } from "./render.js";

const readFormValues = () => {
  return {
    name: getEl("f_name").value.trim(),
    brand: getEl("f_brand").value.trim(),
    sku: getEl("f_sku").value.trim(),
    image_url: getEl("f_image_url").value.trim(),
    price: parseFloat(getEl("f_price").value),
    stock: parseInt(getEl("f_stock").value, 10),
    description: getEl("f_description").value.trim(),
  };
};

const isFormValid = (values) => {
  return (
    Boolean(values.name) &&
    Boolean(values.brand) &&
    !isNaN(values.price) &&
    !isNaN(values.stock)
  );
};

const buildProductPayload = (values) => {
  return {
    name: values.name,
    brand: values.brand,
    image_url: values.image_url,
    price: values.price,
    stock: values.stock,
    description: values.description,
  };
};

export const handleFormSubmit = async (e) => {
  e.preventDefault();
  const values = readFormValues();
  if (!isFormValid(values)) {
    showToast("Please fill in all required fields.");
    return;
  }

  setSavingState(true);
  try {
    if (state.editingProductId) {
      await saveExistingProduct(state.editingProductId, values);
    } else {
      await saveNewProduct(values);
    }
    closePanel();
    renderAll();
  } catch (error) {
    console.error(error);
    showToast("Something went wrong while saving.");
  } finally {
    setSavingState(false);
  }
};

const setSavingState = (isSaving) => {
  getEl("saveBtn").disabled = isSaving;
};

const saveNewProduct = async (values) => {
  const payload = buildProductPayload(values);
  const created = await createProductRequest(payload);
  state.products.push(created);
  showToast("Product added.");
};

const saveExistingProduct = async (id, values) => {
  const existing = findProductById(id);
  const payload = buildProductPayload(values, existing ? existing.sku : "");
  const updated = await updateProductRequest(id, payload);
  replaceProductInState(id, updated);
  showToast("Product updated.");
};

const replaceProductInState = (id, updatedProduct) => {
  const index = state.products.findIndex((product) => product.id === id);
  if (index !== -1) {
    state.products[index] = updatedProduct;
  }
};
