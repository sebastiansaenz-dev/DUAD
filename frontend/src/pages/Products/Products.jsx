import { useEffect, useState } from "react";
import ProductCard from "../../components/ProductCard/ProductCard";
import Loader from "../../components/loading-ui/Loader";
import paginationStyles from "./Pagination.module.css";
import searchSectionStyles from "./SearchSection.module.css";
import mainStyles from "./Main.module.css";
import { getProducts } from "../../api/productsApi";

const Products = ({ setCurrentPage, setSelectedProduct }) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    const timer = setTimeout(() => {
      const nextSearch = searchTerm.trim();
      setDebouncedSearch((prevSearch) => {
        if (prevSearch !== nextSearch) {
          setPage(1);
        }
        return nextSearch;
      });
    }, 350);

    return () => clearTimeout(timer);
  }, [searchTerm]);

  useEffect(() => {
    setLoading(true);
    setError(null);

    getProducts(page, debouncedSearch)
      .then((res) => setData(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [page, debouncedSearch]);

  const handleViewDetail = (product) => {
    setSelectedProduct(product);
    setCurrentPage("product-detail");
  };

  if (loading) {
    return (
      <main className={mainStyles["main"]}>
        <section className={mainStyles["title-section"]}>
          <h1>Catalogo de productos</h1>
        </section>
        <div className={mainStyles["loader-wrap"]}>
          <Loader />
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className={mainStyles["main"]}>
        <section className={mainStyles["title-section"]}>
          <h1>Catalogo de productos</h1>
        </section>
        <p className={mainStyles["error-message"]}>{error}</p>
      </main>
    );
  }

  const products = data?.items ?? [];
  const totalPages = data?.total_pages ?? 0;

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
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {products.length === 0 && (
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
          <p>
            {debouncedSearch
              ? "Intenta cambiar los filtros o la busqueda"
              : "No hay productos disponibles por el momento."}
          </p>
        </div>
      )}

      {products.length > 0 && (
        <>
          <div className={mainStyles["products-container"]}>
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onViewDetails={handleViewDetail}
              />
            ))}
          </div>

          {totalPages > 1 && (
            <div className={paginationStyles["pagination-container"]}>
              <button
                className={paginationStyles["pagination-button"]}
                disabled={page === 1}
                onClick={() => setPage(page - 1)}
              >
                «
              </button>

              {Array.from({ length: totalPages }, (_, index) => {
                const pageNumber = index + 1;
                return (
                  <button
                    key={pageNumber}
                    className={`${paginationStyles["pagination-button"]} ${pageNumber === page ? paginationStyles["active"] : ""}`}
                    onClick={() => setPage(pageNumber)}
                  >
                    {pageNumber}
                  </button>
                );
              })}

              <button
                className={paginationStyles["pagination-button"]}
                disabled={page >= totalPages}
                onClick={() => setPage(page + 1)}
              >
                »
              </button>
            </div>
          )}
        </>
      )}
    </main>
  );
};

export default Products;
