import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CartProvider, useCart } from "./CartContext";
import { render } from "@testing-library/react";

const CartProbe = () => {
  const {
    cart,
    itemCount,
    total,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
  } = useCart();

  return (
    <div>
      <p>cantidad:{itemCount}</p>
      <p>total:{total}</p>
      <ul>
        {cart.map((item) => (
          <li key={item.id}>
            {item.name}:{item.quantity}
          </li>
        ))}
      </ul>
      <button
        onClick={() =>
          addToCart({
            id: 1,
            name: "Juguete",
            price: 5000,
            quantity: 1,
            stock: 5,
          })
        }
      >
        agregar
      </button>
      <button onClick={() => updateQuantity(1, 3)}>cambiar cantidad</button>
      <button onClick={() => removeFromCart(1)}>quitar</button>
      <button onClick={clearCart}>vaciar</button>
    </div>
  );
};

const renderCart = () =>
  render(
    <CartProvider>
      <CartProbe />
    </CartProvider>,
  );

describe("CartContext", () => {
  test("adds a product and persists it in localStorage", async () => {
    const user = userEvent.setup();
    renderCart();

    await user.click(screen.getByRole("button", { name: /agregar/i }));

    expect(screen.getByText("cantidad:1")).toBeInTheDocument();
    expect(screen.getByText("total:5000")).toBeInTheDocument();
    expect(screen.getByText("Juguete:1")).toBeInTheDocument();
    expect(JSON.parse(localStorage.getItem("cart"))[0]).toMatchObject({
      id: 1,
      quantity: 1,
    });
  });

  test("increases quantity when the same product is added again", async () => {
    const user = userEvent.setup();
    renderCart();

    await user.click(screen.getByRole("button", { name: /agregar/i }));
    await user.click(screen.getByRole("button", { name: /agregar/i }));

    expect(screen.getByText("cantidad:2")).toBeInTheDocument();
    expect(screen.getByText("total:10000")).toBeInTheDocument();
  });

  test("updates, removes, and clears cart items", async () => {
    const user = userEvent.setup();
    renderCart();

    await user.click(screen.getByRole("button", { name: /agregar/i }));
    await user.click(screen.getByRole("button", { name: /cambiar cantidad/i }));
    expect(screen.getByText("Juguete:3")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /quitar/i }));
    expect(screen.getByText("cantidad:0")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /agregar/i }));
    await user.click(screen.getByRole("button", { name: /vaciar/i }));
    expect(screen.getByText("cantidad:0")).toBeInTheDocument();
    expect(JSON.parse(localStorage.getItem("cart"))).toEqual([]);
  });
});
