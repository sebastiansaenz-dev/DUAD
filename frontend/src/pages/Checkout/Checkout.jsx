import { useState } from "react";
import styles from "./styles/OrderSummary.module.css";
import errorStyle from "../../utils/errorSections.module.css";
import { useCart } from "../../context/CartContext";
import { formatPrice } from "../../utils/utils";
import { useNavigate } from "react-router-dom";
import { createOrder } from "../../api/orderAPI";

const Checkout = () => {
  const { cart, total, clearCart } = useCart();
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const items = cart ?? [];

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);

    if (items.length === 0) {
      setError("Tu carrito está vacío");
      return;
    }

    const formData = new FormData(e.target);
    const orderData = {
      full_name: formData.get("name")?.trim(),
      email: formData.get("email")?.trim(),
      address: formData.get("address")?.trim(),
      phone: formData.get("phone")?.trim(),
      items: items.map((item) => ({
        id: Number(item.id),
        quantity: Number(item.quantity ?? 1),
      })),
    };

    if (!orderData.full_name || !orderData.address || !orderData.phone) {
      setError("Completa todos los campos del formulario");
      return;
    }

    setSubmitting(true);

    createOrder(orderData)
      .then(() => {
        navigate("/order-confirmed", {
          replace: true,
          state: {
            items,
            total,
          },
        });
        clearCart();
      })
      .catch(() => {
        setError(
          "Ocurrió un problema al procesar tu compra. Por favor intenta de nuevo."
        );
      })
      .finally(() => setSubmitting(false));
  };

  return (
    <main className={styles["checkout-container"]}>
      <h1>Checkout</h1>

      <div className={styles["checkout-grid"]}>
        <section className={styles["checkout-form-section"]}>
          <h2>Información de envío y pago</h2>

          {error && (
            <div className={errorStyle["error-section"]}>
              <span>{error}</span>
            </div>
          )}

          <form id="order-form" onSubmit={handleSubmit}>
            <div className={styles["form-group"]}>
              <label htmlFor="name">Nombre completo</label>
              <input type="text" id="name" name="name" required />
            </div>

            <div className={styles["form-group"]}>
              <label htmlFor="email">Correo electrónico</label>
              <input type="email" id="email" name="email" required />
            </div>

            <div className={styles["form-group"]}>
              <label htmlFor="phone">Teléfono</label>
              <input type="tel" id="phone" name="phone" required />
            </div>

            <div className={styles["form-group"]}>
              <label htmlFor="address">Dirección de envío</label>
              <input type="text" id="address" name="address" required />
            </div>

            <div className={styles["form-group"]}>
              <label htmlFor="payment">Método de pago</label>
              <select id="payment" name="payment" required>
                <option value="card">Sinpe</option>
              </select>
            </div>
          </form>
        </section>

        <section className={styles["checkout-summary-section"]}>
          <h2>Resumen de la compra</h2>

          <div className={styles["summary-items-list"]}>
            {items.length === 0 && <p>El carrito está vacío</p>}
            {items.map((item) => {
              const quantity = Number(item.quantity ?? 1);
              const itemTotal = Number(item.price ?? 0) * quantity;

              return (
                <div key={item.id} className={styles["summary-item"]}>
                  <img src={item.image_url} alt={item.name} />
                  <div className={styles["summary-item-details"]}>
                    <h4>{item.name}</h4>
                    <p>Precio: {formatPrice(item.price)}</p>
                    <p>Cantidad: {quantity}</p>
                  </div>
                  <span className={styles["summary-item-price"]}>
                    {formatPrice(itemTotal)}
                  </span>
                </div>
              );
            })}
          </div>

          <div className={styles["summary-footer"]}>
            <div className={styles["total-line"]}>
              <span>Total a pagar:</span>
              <span className={styles["total-price"]}>
                {formatPrice(total)}
              </span>
            </div>
            <button
              type="submit"
              form="order-form"
              className={styles["confirm-button"]}
              disabled={submitting || items.length === 0}
            >
              {submitting ? "Procesando..." : "Confirmar compra"}
            </button>
          </div>
        </section>
      </div>
    </main>
  );
};

export default Checkout;
