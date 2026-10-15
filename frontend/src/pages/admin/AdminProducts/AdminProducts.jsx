import ProductForm from "../../../components/ProductForm/ProductForm";
import ProductTable from "../../../components/ProductTable/ProductTable";
import { useProductStore } from "../../../store/useProductStore";
import ProductTableStyles from "./styles/ProductsTable.module.css";
import AddProductFormStyles from "./styles/AddProductFormSection.module.css";

const AdminProducts = ({ setCurrentPage, setSelectedProduct }) => {
  const { products, deleteProduct, addProduct } = useProductStore();

  const onSubmit = (data) => {
    addProduct(data);
  };

  const formPlaceholders = {
    name: "Nombre del producto",
    description: "Descripción detallada del producto",
    price: "0.00",
    category: "Categoría del producto (ej. Alimento, Juguetes)",
    image_url: "/api/placehold.co/600x400",
    stock: "0",
  };

  return (
    <main>
      <div className={ProductTableStyles["products-managment-section"]}>
        <section className={ProductTableStyles["title-section"]}>
          <h1>Administración de productos</h1>
          <p>
            En esta sección puedes gestionar el catálogo de productos de
            PawStore
          </p>
        </section>
        <ProductTable
          products={products}
          onEdit={(product) => {
            setSelectedProduct(product);
            setCurrentPage("admin-edit");
          }}
          onDelete={deleteProduct}
        />
      </div>
      <div className={AddProductFormStyles["add-product-form-section"]}>
        <section className={AddProductFormStyles["title-section"]}>
          <h1>Agregar nuevo producto</h1>
        </section>
        <ProductForm
          onSubmit={onSubmit}
          submitButtonText={"Agregar nuevo producto"}
          styles={AddProductFormStyles}
        />
      </div>
    </main>
  );
};

export default AdminProducts;
