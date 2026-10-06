import { useState } from "react";
import ProductCard from "../../components/ProductCard/ProductCard";
import rawProducts from "../../../data/products.json";
import paginationStyles from "./Pagination.module.css";
import searchSectionStyles from "./SearchSection.module.css";
import errorStyles from "../../utils/errorSections.module.css";
import mainStyles from "./Main.module.css";

const adaptProducts = (rawProducts) => {
  return rawProducts.map((product) => ({
    id: product.id,
    name: product.nombre,
    description: product.descripcion,
    price: product.precio,
    category: product.categoria,
    image_url: product.imagen,
    stock: product.stock,
  }));
};

const Products = ({ setCurrentPage, setSelectedProduct }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPageNum] = useState(1);
  const itemsPerPage = 20;

  const products = adaptProducts(rawProducts);

  const handleViewDetail = (product) => {
    setSelectedProduct(product);
    setCurrentPage("product-detail");
  };

  if (!products || products.length === 0) {
    return (
      <div className={errorStyles["error-section"]}>
        No hay productos disponibles por el momento.
      </div>
    );
  }

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  const totalPages = Math.ceil(filteredProducts.length / itemsPerPage);

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentProducts = filteredProducts.slice(
    indexOfFirstItem,
    indexOfLastItem,
  );

  return (
    <main className={mainStyles["main"]}>
      <section className={mainStyles["title-section"]}>
        <h1>Catalogo de productos</h1>
      </section>

      <div className={searchSectionStyles["search-section"]}>
        <input
          type="text"
          placeholder="Buscar producto"
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setCurrentPageNum(1);
          }}
        />
      </div>

      {filteredProducts.length === 0 && (
        <div className={mainStyles["no-results"]}>
          <svg
            className={mainStyles["no-results"]}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            <path
              d="M9 9H9.01"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M15 9H15.01"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            <path
              d="M9 16C9 16 10.5 14.5 12 14.5C13.5 14.5 15 16 15 16"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <h2>No se encontraron productos</h2>
          <p>Intenta cambiar los filtros o la busqueda</p>
        </div>
      )}

      <div className={mainStyles["products-container"]}>
        {currentProducts.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            onViewDetails={handleViewDetail}
          ></ProductCard>
        ))}
      </div>

      {/* PAGINATION */}
      {/* <div className={paginationStyles["pagination-container"]}>
        <button
          className={paginationStyles["pagination-button"]}
          disabled={currentPage === 1}
          onClick={() => setCurrentPageNum(currentPage - 1)}
        >
          «
        </button>

        {Array.from({ length: totalPages }, (_, index) => {
          const pageNumber = index + 1;
          return (
            <button
              key={pageNumber}
              className={`${paginationStyles["pagination-button"]} ${pageNumber === currentPage ? paginationStyles["active"] : ""}`}
              onClick={() => setCurrentPageNum(pageNumber)}
            >
              {pageNumber}
            </button>
          );
        })}

        <button
          className={paginationStyles["pagination-button"]}
          disabled={currentPage >= totalPages || totalPages === 0}
          onClick={() => setCurrentPageNum(currentPage + 1)}
        >
          »
        </button>
      </div> */}
    </main>
  );
};

export default Products;
