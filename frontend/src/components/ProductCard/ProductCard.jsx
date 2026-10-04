import styles from "./ProductCard.module.css";

const ProductCard = ({ product, onViewDetails }) => {
  return (
    <div className={styles["product"]}>
      <img
        className={styles["product-img"]}
        src={product.image_url}
        alt={product.name}
      />
      <div className={styles["product-data-container"]}>
        <h2 className={styles["product-name"]}>{product.name}</h2>
        <span className={styles["product-price"]}>{product.price}</span>
        <p className={styles["product-brand"]}>{product.brand}</p>
      </div>
      <button
        className={styles["view-details-button"]}
        onClick={() => onViewDetails(product)}
      >
        View details
      </button>
    </div>
  );
};

export default ProductCard;
