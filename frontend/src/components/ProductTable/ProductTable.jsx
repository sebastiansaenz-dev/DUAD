import ProductRow from "../ProductRow/ProductRow";
import styles from "./ProductTable.module.css";

const ProductTable = ({ products, onEdit, onDelete }) => {
  return (
    <div className={styles["table"]}>
      <div className={styles["table-rows"]}>
        <span>ID</span>
        <span>NOMBRE</span>
        <span>PRECIO</span>
        <span>CATEGORIA</span>
        <span>STOCK</span>
        <span>ACCIONES</span>
      </div>

      {products.map((product) => (
        <ProductRow
          key={product.id}
          product={product}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export default ProductTable;
