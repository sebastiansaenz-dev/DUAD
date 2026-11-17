import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import styles from "./ProductDetail.module.css";
import { formatPrice } from "../../utils/utils";
import { getProductById } from "../../api/productsApi";
import Loader from "../../components/loading-ui/Loader";
import { useCart } from "../../context/CartContext";

const ProductDetail = () => {
  const { id } = useParams();
  const { addToCart } = useCart();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    setLoading(true);
    setError(null);

    getProductById(id)
      .then((res) => setProduct(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

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
    setSuccessMessage("Producto agregado al carrito!");

    addToCart({ ...product, quantity });

    setTimeout(() => {
      setSuccessMessage("");
    }, 3000);
  };

  if (loading) {
    return (
      <main className={styles["product-container"]}>
        <Loader />
      </main>
    );
  }

  if (error || !product) {
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

        <button
          className={styles["add-to-cart-button"]}
          onClick={handleAddToCart}
        >
          Agregar al carrito
        </button>

        {successMessage && (
          <div className={styles["success-message"]}>{successMessage}</div>
        )}
      </div>
    </main>
  );
};

export default ProductDetail;
