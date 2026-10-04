import { useState } from "react";
import ProductCard from "../../components/ProductCard/ProductCard";
import products from "../../../data/products.json";
import paginationStyles from "./Pagination.module.css";
import searchSectionStyles from "./SearchSection.module.css";
import mainStyles from "./Main.module.css";

const Products = ({ setCurrentPage, setSelectedProduct }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPageNum] = useState(1);
  const itemsPerPage = 20;

  const handleViewDetail = (product) => {
    setSelectedProduct(product);
    setCurrentPage("product-detail");
  };

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
        <h1>Products</h1>
      </section>

      <div className={searchSectionStyles["search-section"]}>
        <input
          type="text"
          placeholder="Search product"
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setCurrentPageNum(1);
          }}
        />
      </div>

      <div className="error-section" id="error-section"></div>

      {filteredProducts.length === 0 && (
        <div id="no-results">No products found</div>
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
      <div className={paginationStyles["pagination-container"]}>
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
              className={`${paginationStyles["pagination-button"]} ${pageNumber === currentPage ? "active" : ""}`}
              onClick={() => setCurrentPageNum(pageNumber)}
            >
              {pageNumber}
            </button>
          );
        })}

        <button
          className={paginationStyles["pagination-button"]}
          disabled={currentPage === totalPages}
          onClick={() => setCurrentPageNum(currentPage + 1)}
        >
          »
        </button>
      </div>
    </main>
  );
};

export default Products;
