import { api } from "./axiosClient";

export const getProducts = (page = 1, name = "", all = false) => {
  if (all) {
    return api.get("/products/?all=true");
  }
  let url = `/products/?page=${page}`;
  if (name) {
    url += `&name=${encodeURIComponent(name)}`;
  }
  return api.get(url);
};

export const getProductById = (id) => {
  return api.get(`/products/${id}`);
};
