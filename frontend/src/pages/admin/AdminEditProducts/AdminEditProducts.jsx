import EditProductForm from "../../../components/EditProductForm/EditProductForm";
import styles from "./styles/AdminEditProducts.module.css";

const AdminEditProducts = ({ product, setCurrentPage }) => {
  return (
    <main className={styles["admin-edit-products"]}>
      <section className={styles["title-section"]}>
        <h1>Editar producto</h1>
      </section>

      <div className={styles["edit-prouct-form"]}>
        <EditProductForm product={product} setCurrentPage={setCurrentPage} />
      </div>
    </main>
  );
};

export default AdminEditProducts;
