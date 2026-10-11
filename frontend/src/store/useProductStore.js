import { create } from "zustand";
import initialProducts from "../../data/products.json";
import { adaptProducts } from "../utils/utils.js";

export const useProductStore = create((set) => ({
  products: adaptProducts(initialProducts),

  addProduct: (newProduct) =>
    set((state) => {
      const [adaptedNewProduct] = adaptProducts([newProduct]);

      const productWithId = {
        ...adaptedNewProduct,
        id: `${state.products.length + 1}`,
      };

      return {
        products: [...state.products, productWithId],
      };
    }),

  updateProduct: (updatedProduct) =>
    set((state) => ({
      products: state.products.map((product) =>
        product.id === updatedProduct.id ? updatedProduct : product,
      ),
    })),

  deleteProduct: (id) =>
    set((state) => ({
      products: state.products.filter((product) => product.id !== id),
    })),
}));
