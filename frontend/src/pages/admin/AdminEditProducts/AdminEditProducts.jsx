import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import ProductForm from "../../../components/ProductForm/ProductForm";
import styles from "./styles/AdminEditProducts.module.css";
import EditProductFormStyles from "./styles/EditProductForm.module.css";
import errorStyle from "../../../utils/errorSections.module.css";
import { updateProduct } from "../../../api/admin/adminProductsApi.js";
import { getProductById } from "../../../api/productsApi.js";
import Loader from "../../../components/loading-ui/Loader.jsx";

const AdminEditProducts = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    getProductById(id)
      .then((res) => setProduct(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  const onSubmit = (data) => {
    setError(null);
    updateProduct(product.id, data)
      .then(() => navigate("/admin"))
      .catch((err) =>
        setError(err.response?.data?.error?.message || err.message)
      );
  };

  if (loading) {
    return (
      <main className={styles["admin-edit-products"]}>
        <Loader />
      </main>
    );
  }

  if (error && !product) {
    return (
      <div className={errorStyle["error-section"]}>
        <span>{error}</span>
      </div>
    );
  }

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
          onCancel={() => navigate("/admin")}
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
