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
import { useAuthStore } from "./store/useAuthStore.js";

import errorStyle from "./utils/errorSections.module.css";

const App = () => {
  const currentPage = usePageStore((state) => state.currentPage);
  const setCurrentPage = usePageStore((state) => state.setCurrentPage);
  const [selectedProduct, setSelectedProduct] = useState(null);

  const user = useAuthStore((state) => state.user);
  const roles = user?.user?.roles ?? [];
  const isAdmin = roles.some((role) => role.name === "admin");

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
      {currentPage === "administration" && isAdmin && (
        <AdminProducts
          setCurrentPage={setCurrentPage}
          setSelectedProduct={setSelectedProduct}
        />
      )}

      {currentPage === "administration" && !isAdmin && (
        <div className={errorStyle["error-section"]}>
          <span>No tienes permisos para acceder a esta página</span>
        </div>
      )}

      {currentPage === "admin-edit" && isAdmin && (
        <AdminEditProducts
          product={selectedProduct}
          setCurrentPage={setCurrentPage}
        />
      )}

      {currentPage === "admin-edit" && !isAdmin && (
        <div className={errorStyle["error-section"]}>
          <span>No tienes permisos para acceder a esta página</span>
        </div>
      )}

      {currentPage === "login" && <Login setCurrentPage={setCurrentPage} />}

      <Footer setCurrentPage={setCurrentPage} />
    </>
  );
};

export default App;
