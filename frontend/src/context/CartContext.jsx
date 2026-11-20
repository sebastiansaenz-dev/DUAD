import { createContext, useContext, useState } from "react";

const CartContext = createContext(null);

const persistCart = (nextCart, setCart) => {
  setCart(nextCart);
  localStorage.setItem("cart", JSON.stringify(nextCart));
};

const mergeCartItems = (items) => {
  const byId = new Map();

  for (const item of items) {
    const id = Number(item.id);
    const prev = byId.get(id);
    const quantity = Number(item.quantity) || 1;

    if (!prev) {
      byId.set(id, { ...item, id, quantity });
      continue;
    }

    const stock = Number(prev.stock ?? item.stock) || 100;
    byId.set(id, {
      ...prev,
      quantity: Math.min((Number(prev.quantity) || 1) + quantity, stock),
    });
  }

  return [...byId.values()];
};

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(() => {
    try {
      return mergeCartItems(JSON.parse(localStorage.getItem("cart")) ?? []);
    } catch {
      return [];
    }
  });

  const addToCart = (product) => {
    const quantityToAdd = Number(product.quantity) || 1;
    const productId = Number(product.id);
    const stock = Number(product.stock) || quantityToAdd;

    const existing = cart.find((item) => Number(item.id) === productId);

    if (existing) {
      const nextQuantity = Math.min(
        Number(existing.quantity ?? 1) + quantityToAdd,
        Number(existing.stock ?? stock),
      );
      const newCart = cart.map((item) =>
        Number(item.id) === productId
          ? { ...item, quantity: nextQuantity }
          : item,
      );
      persistCart(newCart, setCart);
      return;
    }

    persistCart(
      [...cart, { ...product, id: productId, quantity: quantityToAdd }],
      setCart,
    );
  };

  const removeFromCart = (productId) => {
    const newCart = cart.filter(
      (item) => Number(item.id) !== Number(productId),
    );
    persistCart(newCart, setCart);
  };

  const updateQuantity = (productId, quantity) => {
    const item = cart.find((cartItem) => Number(cartItem.id) === Number(productId));
    if (!item) {
      return;
    }

    const stock = Number(item.stock) || 100;
    const nextQuantity = Math.min(Math.max(Number(quantity) || 1, 1), stock);

    const newCart = cart.map((cartItem) =>
      Number(cartItem.id) === Number(productId)
        ? { ...cartItem, quantity: nextQuantity }
        : cartItem,
    );
    persistCart(newCart, setCart);
  };

  const clearCart = () => {
    persistCart([], setCart);
  };

  const itemCount = cart.reduce(
    (sum, item) => sum + (Number(item.quantity) || 1),
    0,
  );

  const total = cart.reduce(
    (sum, item) =>
      sum + Number(item.price ?? 0) * Number(item.quantity ?? 1),
    0,
  );

  const value = {
    cart,
    itemCount,
    total,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
};
