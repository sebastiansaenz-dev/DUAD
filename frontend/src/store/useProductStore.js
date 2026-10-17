import { create } from "zustand";
import initialProducts from "../../data/products.json";
import { adaptProducts } from "../utils/utils.js";

export const useProductStore = create((set) => ({
  products: adaptProducts(initialProducts),

  addProduct: (newProduct) =>
    set((state) => {
      const [adaptedNewProduct] = adaptProducts([newProduct]);

      const newId =
        state.products.reduce(
          (max, product) => (product.id > max ? product.id : max),
          0,
        ) + 1;

      const productWithId = {
        ...adaptedNewProduct,
        id: newId,
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
