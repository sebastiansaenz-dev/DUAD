import ProductForm from "../../../components/ProductForm/ProductForm";
import styles from "./styles/AdminEditProducts.module.css";
import EditProductFormStyles from "./styles/EditProductForm.module.css";
import { useProductStore } from "../../../store/useProductStore";

const AdminEditProducts = ({ product, setCurrentPage }) => {
  const { updateProduct } = useProductStore();

  const onSubmit = (data) => {
    const formattedProduct = {
      id: Number(product.id),
      name: data.name,
      description: data.description,
      price: Number(data.price),
      category: data.category,
      image_url: data.image,
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
          errorMessage={
            "Por favor completa todos los campos antes de guardar los cambios."
          }
        />
      </div>
    </main>
  );
};

export default AdminEditProducts;
