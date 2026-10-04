import { useState } from "react";
import styles from "./ProductDetail.module.css";

const ProductDetail = ({ product }) => {
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

  const handleQuuantityChange = (e) => {
    const value = parseInt(e.target.value, 10);
    if (isNaN(value) || value < 1) {
      setQuantity(1);
    } else if (value > 100) {
      setQuantity(100);
    } else {
      setQuantity(value);
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
          <span className={styles["product-brand"]}>{product.brand}</span>
          <h1 className={styles["product-name"]}>{product.name}</h1>
          <span className={styles["product-price"]}>{product.price}</span>
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
            onChange={handleQuuantityChange}
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

        <button
          className={styles["add-to-cart-button"]}
          onClick={handleAddToCart}
        >
          Add to cart
        </button>

        {successMessage && (
          <div className={styles["success-message"]}>{successMessage}</div>
        )}
      </div>
    </main>
  );
};

export default ProductDetail;
