import { state } from "./state.js";

export const findProductById = (id) => {
  return state.products.find((product) => product.id === id);
};

export const getCategoryCounts = () => {
  const counts = {};
  state.products.forEach((product) => {
    counts[product.category] = (counts[product.category] || 0) + 1;
  });
  return counts;
};

export const matchesCategoryFilter = (product) => {
  return (
    state.currentCategoryFilter === "all" ||
    product.category === state.currentCategoryFilter
  );
};

export const getFilteredProducts = () => {
  return state.products.filter((product) => matchesCategoryFilter(product));
};
