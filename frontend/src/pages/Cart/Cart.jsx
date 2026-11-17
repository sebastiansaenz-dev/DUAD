import styles from "./styles/Cart.module.css";
import { useCart } from "../../context/CartContext";
import { formatPrice } from "../../utils/utils";
import { useNavigate } from "react-router-dom";

const Cart = () => {
  const { cart, removeFromCart, updateQuantity } = useCart();
  const navigate = useNavigate();
  const items = cart ?? [];
  const total = items.reduce(
    (sum, item) => sum + Number(item.price ?? 0) * Number(item.quantity ?? 1),
    0
  );

  return (
    <main className={styles["cart-container"]}>
      <header className={styles["cart-header"]}>
        <h1>Tu carrito</h1>
        <p>
          {items.length === 0
            ? "Aún no has agregado productos"
            : `${items.length} producto${items.length === 1 ? "" : "s"}`}
        </p>
      </header>

      <div className={styles["cart-items-list"]}>
        {items.length === 0 && (
          <div className={styles["empty-cart"]}>
            <p>Tu carrito está vacío</p>
            <span>Explora el catálogo y agrega algo para tu mascota.</span>
          </div>
        )}

        {items.map((item) => {
          const quantity = Number(item.quantity ?? 1);
          const price = Number(item.price ?? 0);
          const itemTotal = price * quantity;

          return (
            <div key={item.id} className={styles["cart-item"]}>
              <div className={styles["product-img"]}>
                <img src={item.image_url} alt={item.name} />
              </div>
              <div className={styles["cart-item-details"]}>
                <h4>{item.name}</h4>
                <span className={styles["item-id"]}>ID: {item.id}</span>
                <div className={styles["item-meta"]}>
                  <div className={styles["qty-controls"]}>
                    <button
                      type="button"
                      className={styles["qty-btn"]}
                      disabled={quantity <= 1}
                      onClick={() => updateQuantity(item.id, quantity - 1)}
                    >
                      −
                    </button>
                    <span className={styles["qty-value"]}>{quantity}</span>
                    <button
                      type="button"
                      className={styles["qty-btn"]}
                      disabled={
                        item.stock != null && quantity >= Number(item.stock)
                      }
                      onClick={() => updateQuantity(item.id, quantity + 1)}
                    >
                      +
                    </button>
                  </div>
                  <span>
                    Precio <strong>{formatPrice(price)}</strong>
                  </span>
                </div>
                <p className={styles["item-total"]}>
                  Subtotal {formatPrice(itemTotal)}
                </p>
              </div>
              <button
                className={styles["remove-btn"]}
                onClick={() => removeFromCart(item.id)}
              >
                Quitar
              </button>
            </div>
          );
        })}
      </div>

      {items.length > 0 && (
        <div className={styles["cart-summary"]}>
          <h3>
            Total <span>{formatPrice(total)}</span>
          </h3>
          <button
            className={styles["checkout-button"]}
            onClick={() => navigate("/checkout")}
          >
            Ir al checkout
          </button>
        </div>
      )}
    </main>
  );
};

export default Cart;
