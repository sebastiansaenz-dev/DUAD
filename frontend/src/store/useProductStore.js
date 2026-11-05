import { create } from "zustand";

export const useProductStore = create((set) => ({
  products: [],

  addProduct: (newProduct) =>
    set((state) => {
      const newId =
        state.products.reduce(
          (max, product) => (product.id > max ? product.id : max),
          0
        ) + 1;

      return {
        products: [...state.products, { ...newProduct, id: newId }],
      };
    }),

  updateProduct: (updatedProduct) =>
    set((state) => ({
      products: state.products.map((product) =>
        product.id === updatedProduct.id ? updatedProduct : product
      ),
    })),

  deleteProduct: (id) =>
    set((state) => ({
      products: state.products.filter((product) => product.id !== id),
    })),
}));
