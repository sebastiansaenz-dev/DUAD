import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render } from "@testing-library/react";
import { AuthProvider } from "../context/AuthContext";
import { CartProvider } from "../context/CartContext";

export const sampleProduct = {
  id: 2,
  name: "Cama para perro",
  price: 15000,
  quantity: 1,
  stock: 10,
  image_url: "https://example.com/bed.jpg",
};

export const renderWithProviders = (
  ui,
  { cart = [], user = null, route = "/", routes } = {},
) => {
  localStorage.setItem("cart", JSON.stringify(cart));

  if (user) {
    localStorage.setItem("user", JSON.stringify(user));
  } else {
    localStorage.removeItem("user");
  }

  return render(
    <MemoryRouter initialEntries={[route]}>
      <AuthProvider>
        <CartProvider>
          {routes ?? ui}
        </CartProvider>
      </AuthProvider>
    </MemoryRouter>,
  );
};

export const AppRoutes = ({ children }) => (
  <Routes>
    {children}
  </Routes>
);
