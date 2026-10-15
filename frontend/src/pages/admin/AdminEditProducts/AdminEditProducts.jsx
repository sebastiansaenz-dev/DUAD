import ProductForm from "../../../components/ProductForm/ProductForm";
import styles from "./styles/AdminEditProducts.module.css";
import EditProductFormStyles from "./styles/EditProductForm.module.css";

const AdminEditProducts = ({ product, setCurrentPage }) => {
  const onSubmit = (data) => {
    const formattedProduct = {
      id: Number(product.id),
      name: data.nombre,
      description: data.descripcion,
      price: Number(data.precio),
      category: data.categoria,
      image_url: data.imagen,
      stock: Number(data.stock),
    };

    updateProduct(formattedProduct);
    setCurrentPage("administration");
  };

  const onCancel = () => {
    setCurrentPage("administration");
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
          onCancel={onCancel}
          styles={EditProductFormStyles}
        />
      </div>
    </main>
  );
};

export default AdminEditProducts;
