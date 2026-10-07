import { useState } from "react";
import styles from "./ProductDetail.module.css";
import { formatPrice } from "../../utils/utils";

const ProductDetail = ({ product, setCurrentPage }) => {
  const [quantity, setQuantity] = useState(1);
  const [successMessage, setSuccessMessage] = useState("");

  const handleQuantityDecrease = () => {
    if (quantity > 1) {
      setQuantity(quantity - 1);
    }
  };

  const handleQuantityIncrease = () => {
    if (quantity < 100) {
      setQuantity(quantity + 1);
    }
  };

  const handleQuantityChange = (e) => {
    const rawValue = e.target.value;

    if (rawValue === "") {
      setQuantity("");
      return;
    }

    const value = parseInt(rawValue, 10);

    if (!isNaN(value)) {
      if (value > product.stock) {
        setQuantity(product.stock);
      } else if (value < 1) {
        setQuantity(1);
      } else {
        setQuantity(value);
      }
    }
  };

  const handleAddToCart = () => {
    setSuccessMessage("Product added to cart!");

    setTimeout(() => {
      setSuccessMessage("");
    }, 3000);
  };

  if (!product) {
    return <div className={styles["error-section"]}>Product not found</div>;
  }

  return (
    <main className={styles["product-container"]}>
      <div className={styles["product-img"]}>
        <img src={product.image_url} alt={product.name} />
      </div>

      <div className={styles["product-details"]}>
        <div className={styles["product-info"]}>
          <h1 className={styles["product-name"]}>{product.name}</h1>
          <span className={styles["product-price"]}>
            {formatPrice(product.price)}
          </span>
          <span className={styles["product-category"]}>{product.category}</span>
          <p className={styles["product-description"]}>{product.description}</p>
        </div>

        <div className={styles["quantity-selector"]}>
          <button
            className={styles["quantity-btn"]}
            onClick={handleQuantityDecrease}
          >
            −
          </button>
          <input
            type="number"
            className={styles["quantity-input"]}
            value={quantity}
            onChange={handleQuantityChange}
            min="1"
            max="100"
          />
          <button
            className={styles["quantity-btn"]}
            onClick={handleQuantityIncrease}
          >
            +
          </button>
        </div>

        <p>
          Más adelante aquí se podrá agregar este producto al carrito y
          completar la compra
        </p>
        {/* ADD TO CART BUTTON */}
        {/* <button
          className={styles["add-to-cart-button"]}
          onClick={handleAddToCart}
        >
          Add to cart
        </button> */}
        <button
          className={styles["add-to-cart-button"]}
          onClick={(e) => {
            e.preventDefault();
            setCurrentPage("products");
          }}
        >
          Volver al catálogo
        </button>

        {/* SUCCESS MESSAGE */}
        {/* {successMessage && (
          <div className={styles["success-message"]}>{successMessage}</div>
        )} */}
      </div>
    </main>
  );
};

export default ProductDetail;
