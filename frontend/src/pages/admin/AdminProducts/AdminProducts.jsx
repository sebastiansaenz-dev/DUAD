import ProductForm from "../../../components/ProductForm/ProductForm";
import ProductTable from "../../../components/ProductTable/ProductTable";
import ProductTableStyles from "./styles/ProductsTable.module.css";
import AddProductFormStyles from "./styles/AddProductFormSection.module.css";
import { useState, useEffect } from "react";
import { getProducts } from "../../../api/productsApi.js";
import {
  createProduct,
  deleteProduct,
} from "../../../api/admin/adminProductsApi.js";
import Loader from "../../../components/loading-ui/Loader.jsx";

const AdminProducts = ({ setCurrentPage, setSelectedProduct }) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    getProducts(1, "", true)
      .then((response) => setData(response.data))
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading)
    return (
      <div className={ProductTableStyles["loader-wrap"]}>
        <Loader />
      </div>
    );
  if (error) return <span>{error}</span>;

  const products = data?.items ?? [];

  const onSubmit = (data) => {
    createProduct(data)
      .then(() => getProducts(1, "", true))
      .then((response) => setData(response.data))
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false));
  };

  return (
    <main>
      <div className={ProductTableStyles["products-managment-section"]}>
        <section className={ProductTableStyles["title-section"]}>
          <h1>Administración de productos</h1>
          <p>
            En esta sección puedes gestionar el catálogo de productos de
            PawStore.
          </p>
        </section>
        <ProductTable
          products={products}
          onEdit={(product) => {
            setSelectedProduct(product);
            setCurrentPage("admin-edit");
          }}
          onDelete={(id) => {
            deleteProduct(id)
              .then(() => getProducts(1, "", true))
              .then((response) => setData(response.data))
              .catch((error) => setError(error.message));
          }}
        />
      </div>
      <div className={AddProductFormStyles["add-product-form-section"]}>
        <section className={AddProductFormStyles["title-section"]}>
          <h2>Agregar nuevo producto</h2>
        </section>
        <ProductForm
          onSubmit={onSubmit}
          submitButtonText={"Agregar producto"}
          styles={AddProductFormStyles}
          resetAfterSubmit={true}
          errorMessage={
            "Por favor completa todos los campos antes de agregar el producto."
          }
        />
      </div>
    </main>
  );
};

export default AdminProducts;
