import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ProductCard from "../../components/ProductCard/ProductCard";
import Loader from "../../components/loading-ui/Loader";
import paginationStyles from "./Pagination.module.css";
import searchSectionStyles from "./SearchSection.module.css";
import mainStyles from "./Main.module.css";
import { getProducts } from "../../api/productsApi";
import EmptyState from "../../components/EmptyState/EmptyState";

const Products = () => {
  const navigate = useNavigate();
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
      .catch((err) => setError("No hay productos disponibles por el momento."))
      .finally(() => setLoading(false));
  }, [page, debouncedSearch]);

  const handleViewDetail = (product) => {
    navigate(`/products/${product.id}`);
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
        <EmptyState
          title={error}
          message="Intenta recargar la página en unos minutos."
        />
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
        <EmptyState
          title="No se encontraron productos"
          message={
            debouncedSearch
              ? "Intenta cambiar los filtros o la busqueda"
              : "No hay productos disponibles por el momento."
          }
        />
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
