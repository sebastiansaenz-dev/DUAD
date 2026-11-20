import { screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render } from "@testing-library/react";
import OrderConfirmed from "./OrderConfirmed";
import { CartProvider } from "../../context/CartContext";
import { sampleProduct } from "../../test/test-utils";

const renderConfirmed = (entry) =>
  render(
    <MemoryRouter initialEntries={[entry]}>
      <CartProvider>
        <Routes>
          <Route path="/order-confirmed" element={<OrderConfirmed />} />
          <Route path="/productos" element={<p>Catálogo</p>} />
        </Routes>
      </CartProvider>
    </MemoryRouter>,
  );

describe("OrderConfirmed", () => {
  test("redirects to the catalog when opened without order data", () => {
    renderConfirmed("/order-confirmed");

    expect(screen.getByText("Catálogo")).toBeInTheDocument();
    expect(
      screen.queryByText(/gracias por tu compra/i),
    ).not.toBeInTheDocument();
  });

  test("shows the order summary from navigate state", () => {
    renderConfirmed({
      pathname: "/order-confirmed",
      state: {
        items: [sampleProduct],
        total: 15000,
      },
    });

    expect(screen.getByText(/gracias por tu compra/i)).toBeInTheDocument();
    expect(screen.getByText("Cama para perro")).toBeInTheDocument();
    expect(screen.getByText(/cantidad:\s*1/i)).toBeInTheDocument();
  });
});
