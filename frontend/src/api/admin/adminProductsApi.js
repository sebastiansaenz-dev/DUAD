import { apiAuth } from "../axiosClient";

export const createProduct = (productData) => {
  return apiAuth.post("products/", productData);
};

export const updateProduct = (id, productData) => {
  return apiAuth.patch(`products/${id}`, productData);
};

export const deleteProduct = (id) => {
  return apiAuth.delete(`products/${id}`);
};
