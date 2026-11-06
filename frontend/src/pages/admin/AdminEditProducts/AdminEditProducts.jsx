import { useState } from "react";
import ProductForm from "../../../components/ProductForm/ProductForm";
import styles from "./styles/AdminEditProducts.module.css";
import EditProductFormStyles from "./styles/EditProductForm.module.css";
import errorStyle from "../../../utils/errorSections.module.css";
import { updateProduct } from "../../../api/admin/adminProductsApi.js";

const AdminEditProducts = ({ product, setCurrentPage }) => {
  const [error, setError] = useState(null);

  const onSubmit = (data) => {
    setError(null);
    updateProduct(product.id, data)
      .then(() => setCurrentPage("administration"))
      .catch((err) =>
        setError(err.response?.data?.error?.message || err.message),
      );
  };

  return (
    <main className={styles["admin-edit-products"]}>
      <section className={styles["title-section"]}>
        <h1>Editar producto</h1>
      </section>

      <div className={styles["edit-prouct-form"]}>
        {error && (
          <div className={errorStyle["error-section"]}>
            <span>{error}</span>
          </div>
        )}
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
