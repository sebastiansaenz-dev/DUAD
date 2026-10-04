import { api } from "../../../utils/utils.js";
import { isLikelySku } from "./constants.js";
import { state } from "./state.js";

const buildProductsUrl = (page, term) => {
  const params = new URLSearchParams({
    page: page,
  });

  const trimmedTerm = (term || "").trim();
  if (trimmedTerm) {
    if (isLikelySku(trimmedTerm)) {
      params.set("sku", trimmedTerm);
    } else {
      params.set("name", trimmedTerm);
    }
  }

  return `/products/?${params.toString()}`;
};

// GET
export const getProducts = async (page, term) => {
  try {
    const url = buildProductsUrl(page, term);
    const response = await api.get(url);

    state.products = response.data.items;
    state.totalPages =
      response.data.total_pages != null ? response.data.total_pages : 1;

    return state.products;
  } catch (error) {
    console.error(error);
  }
};

// POST
export const createProductRequest = async (productData) => {
  const url = `/staff-portal/products/`;
  const response = await api.post(url, productData);
  return response.data;
};

// PATCH
export const updateProductRequest = async (id, payload) => {
  const url = `/staff-portal/products/${id}`;
  const response = await api.patch(url, payload);
  return response.data;
};

// DELETE
export const deleteProductRequest = async (id) => {
  const url = `/staff-portal/products/${id}`;
  const response = await api.delete(url);
  return response.data;
};
