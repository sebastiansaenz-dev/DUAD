import AddProductForm from "../../../components/AddProductForm/AddProductForm";
import ProductTable from "../../../components/ProductTable/ProductTable";
import { useProductStore } from "../../../store/useProductStore";
import ProductTableStyles from "./styles/ProductsTable.module.css";
import AddProductFormStyles from "./styles/AddProductFormSection.module.css";

const AdminProducts = ({ setCurrentPage, setSelectedProduct }) => {
  const { products: productsObj, deleteProduct } = useProductStore();

  const products = Object.values(productsObj);

  return (
    <main>
      <div className={ProductTableStyles["products-managment-section"]}>
        <section className={ProductTableStyles["title-section"]}>
          <h1>Administración de productos</h1>
          <p>
            En esta seccion puedes gestionar el catalogo de productos de
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
          <h1>Agregar producto</h1>
        </section>
        <AddProductForm />
      </div>
    </main>
  );
};

export default AdminProducts;
