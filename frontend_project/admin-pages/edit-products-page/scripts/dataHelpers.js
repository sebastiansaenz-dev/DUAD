import { state } from "./state.js";

export const findProductById = (id) => {
  return state.products.find((product) => product.id === id);
};

export const getBrandCounts = () => {
  const counts = {};
  state.products.forEach((product) => {
    counts[product.brand] = (counts[product.brand] || 0) + 1;
  });
  return counts;
};

export const matchesBrandFilter = (product) => {
  return (
    state.currentBrandFilter === "all" ||
    product.brand === state.currentBrandFilter
  );
};

export const getFilteredProducts = () => {
  return state.products.filter((product) => matchesBrandFilter(product));
};
