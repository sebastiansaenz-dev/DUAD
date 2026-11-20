import styles from "./styles/OrderConfirmed.module.css";
import { Link, Navigate, useLocation } from "react-router-dom";
import { formatPrice } from "../../utils/utils";

const OrderConfirmed = () => {
  const { state } = useLocation();
  const items = state?.items;
  const total = state?.total;

  if (!items) {
    return <Navigate to="/productos" replace />;
  }

  return (
    <main className={styles["confirmation-container"]}>
      <div className={styles["success-icon-wrapper"]}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="64"
          height="64"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#27ae60"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          className={styles["success-icon"]}
        >
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
      </div>

      <h1 className={styles["confirmation-title"]}>¡Gracias por tu compra!</h1>

      <div id="error-section" className={styles["error-section"]}></div>

      <p className={styles["confirmation-message"]}>
        Hemos enviado un correo de confirmación con los detalles de tu pedido.
      </p>

      <section className={styles["confirmation-summary-box"]}>
        <h2>Resumen de la orden</h2>
        <div className={styles["summary-items-list"]}>
          {items.length === 0 && <p>No hay productos en este pedido</p>}
          {items.map((item) => {
            const quantity = Number(item.quantity ?? 1);
            const itemTotal = Number(item.price ?? 0) * quantity;

            return (
              <div key={item.id} className={styles["summary-item"]}>
                <img src={item.image_url} alt={item.name} />
                <div className={styles["summary-item-details"]}>
                  <h4>{item.name}</h4>
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
            <span className={styles["total-label"]}>Total pagado:</span>
            <span className={styles["total-price"]}>{formatPrice(total)}</span>
          </div>
        </div>
      </section>

      <div className={styles["confirmation-actions"]}>
        <Link
          to="/productos"
          replace
          id="back-to-products-button"
          className={styles["go-back-button"]}
        >
          Volver al catálogo
        </Link>
      </div>
    </main>
  );
};

export default OrderConfirmed;
