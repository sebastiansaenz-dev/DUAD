import { useState } from "react";
import Home from "./pages/Home/Home.jsx";
import Navbar from "./components/Navbar/Navbar.jsx";
import Footer from "./components/Footer/Footer.jsx";
import Products from "./pages/Products/Products.jsx";
import ProductDetail from "./pages/ProductDetail/ProductDetail.jsx";
import AdminProducts from "./pages/admin/AdminProducts/AdminProducts.jsx";
import AdminEditProducts from "./pages/admin/AdminEditProducts/AdminEditProducts.jsx";
import "./App.css";
import Login from "./pages/Login/Login.jsx";
import { usePageStore } from "./store/usePageStore";

const App = () => {
  const currentPage = usePageStore((state) => state.currentPage);
  const setCurrentPage = usePageStore((state) => state.setCurrentPage);
  const [selectedProduct, setSelectedProduct] = useState(null);
  return (
    <>
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      {currentPage === "home" && <Home setCurrentPage={setCurrentPage} />}
      {currentPage === "products" && (
        <Products
          setCurrentPage={setCurrentPage}
          setSelectedProduct={setSelectedProduct}
        />
      )}
      {currentPage === "product-detail" && (
        <ProductDetail
          product={selectedProduct}
          setCurrentPage={setCurrentPage}
        />
      )}
      {currentPage === "administration" && (
        <AdminProducts
          setCurrentPage={setCurrentPage}
          setSelectedProduct={setSelectedProduct}
        />
      )}

      {currentPage === "admin-edit" && (
        <AdminEditProducts
          product={selectedProduct}
          setCurrentPage={setCurrentPage}
        />
      )}

      {currentPage === "login" && <Login setCurrentPage={setCurrentPage} />}

      <Footer setCurrentPage={setCurrentPage} />
    </>
  );
};

export default App;
