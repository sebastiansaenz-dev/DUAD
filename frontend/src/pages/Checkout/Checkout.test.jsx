import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Route, Routes } from "react-router-dom";
import { vi } from "vitest";
import Checkout from "./Checkout";
import { renderWithProviders, sampleProduct } from "../../test/test-utils";

vi.mock("../../api/orderAPI", () => ({
  createOrder: vi.fn(),
}));

import { createOrder } from "../../api/orderAPI";

const fillCheckoutForm = async (user) => {
  await user.type(screen.getByLabelText(/nombre completo/i), "Ana Pérez");
  await user.type(screen.getByLabelText(/correo electrónico/i), "ana@test.com");
  await user.type(screen.getByLabelText(/teléfono/i), "88888888");
  await user.type(
    screen.getByLabelText(/dirección de envío/i),
    "San José, Costa Rica",
  );
};

const renderCheckout = ({ cart = [sampleProduct], user = null } = {}) =>
  renderWithProviders(
    <Routes>
      <Route path="/checkout" element={<Checkout />} />
      <Route path="/order-confirmed" element={<p>Pedido confirmado</p>} />
    </Routes>,
    { cart, user, route: "/checkout" },
  );

describe("Checkout", () => {
  beforeEach(() => {
    createOrder.mockReset();
  });

  test("disables confirm purchase when the cart is empty", () => {
    renderCheckout({ cart: [] });

    expect(screen.getByText(/el carrito está vacío/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /confirmar compra/i }),
    ).toBeDisabled();
  });

  test("submits an order, clears the cart, and navigates to confirmation", async () => {
    const user = userEvent.setup();
    createOrder.mockResolvedValue({ data: { id: 1 } });

    renderCheckout();
    await fillCheckoutForm(user);
    await user.click(screen.getByRole("button", { name: /confirmar compra/i }));

    await screen.findByText("Pedido confirmado");

    expect(createOrder).toHaveBeenCalledTimes(1);
    expect(createOrder).toHaveBeenCalledWith(
      expect.objectContaining({
        full_name: "Ana Pérez",
        email: "ana@test.com",
        phone: "88888888",
        address: "San José, Costa Rica",
        items: [{ id: 2, quantity: 1 }],
      }),
    );
    expect(JSON.parse(localStorage.getItem("cart"))).toEqual([]);
  });

  test("sends the same createOrder request when the user is logged in", async () => {
    const user = userEvent.setup();
    createOrder.mockResolvedValue({ data: { id: 1 } });

    renderCheckout({
      user: { access_token: "token", user: { username: "ana", roles: [] } },
    });
    await fillCheckoutForm(user);
    await user.click(screen.getByRole("button", { name: /confirmar compra/i }));

    await screen.findByText("Pedido confirmado");

    expect(createOrder).toHaveBeenCalledTimes(1);
  });

  test("shows an error and keeps the cart if the order fails", async () => {
    const user = userEvent.setup();
    createOrder.mockRejectedValue(new Error("network"));

    renderCheckout();
    await fillCheckoutForm(user);
    await user.click(screen.getByRole("button", { name: /confirmar compra/i }));

    expect(
      await screen.findByText(
        /ocurrió un problema al procesar tu compra/i,
      ),
    ).toBeInTheDocument();
    expect(screen.queryByText("Pedido confirmado")).not.toBeInTheDocument();
    expect(JSON.parse(localStorage.getItem("cart"))).toEqual([sampleProduct]);
  });

  test("does not call the API when checkout form fields are missing", async () => {
    renderCheckout();

    const form = document.getElementById("order-form");
    form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));

    await waitFor(() => {
      expect(
        screen.getByText(/completa todos los campos del formulario/i),
      ).toBeInTheDocument();
    });
    expect(createOrder).not.toHaveBeenCalled();
  });
});
