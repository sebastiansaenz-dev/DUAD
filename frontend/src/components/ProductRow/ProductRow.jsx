import styles from "./ProductRow.module.css";
import { formatPrice } from "../../utils/utils";

const ProductRow = ({ product, onEdit, onDelete }) => {
  return (
    <div className={styles["product"]}>
      <span className={styles["product-data"]}>{product.id}</span>
      <span className={styles["product-data"]}>{product.name}</span>
      <span className={styles["product-data"]}>
        {formatPrice(product.price)}
      </span>
      <span className={styles["product-data"]}>{product.category}</span>
      <span className={styles["product-data"]}>{product.stock}</span>
      <div className={styles["actions"]}>
        <button onClick={() => onEdit(product)}>Editar</button>
        <button onClick={() => onDelete(product.id)}>Eliminar</button>
      </div>
    </div>
  );
};

export default ProductRow;
