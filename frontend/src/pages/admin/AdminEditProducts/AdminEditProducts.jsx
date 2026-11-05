import ProductForm from "../../../components/ProductForm/ProductForm";
import styles from "./styles/AdminEditProducts.module.css";
import EditProductFormStyles from "./styles/EditProductForm.module.css";
import { useProductStore } from "../../../store/useProductStore";
import { updateProduct } from "../../../api/admin/adminProductsApi.js";

const AdminEditProducts = ({ product, setCurrentPage }) => {
  const onSubmit = (data) => {
    updateProduct(product.id, data)
      .then(() => setCurrentPage("administration"))
      .catch((error) => setError(error.message));
  };

  return (
    <main className={styles["admin-edit-products"]}>
      <section className={styles["title-section"]}>
        <h1>Editar producto</h1>
      </section>

      <div className={styles["edit-prouct-form"]}>
        <ProductForm
          initialValues={product}
          onSubmit={onSubmit}
          submitButtonText={"Guardar cambios"}
          onCancel={() => setCurrentPage("administration")}
          styles={EditProductFormStyles}
          errorMessage={
            "Por favor completa todos los campos antes de guardar los cambios."
          }
        />
      </div>
    </main>
  );
};

export default AdminEditProducts;
